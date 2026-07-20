import logging
import os
from collections import Counter
from datetime import datetime, timedelta, timezone
from urllib.parse import urlparse

import requests


logger = logging.getLogger(__name__)

RIPE_ATLAS_BASE_URL = "https://atlas.ripe.net/api/v2"
RIPE_ATLAS_PROBES_URL = f"{RIPE_ATLAS_BASE_URL}/probes"
RIPE_ATLAS_MEASUREMENTS_URL = f"{RIPE_ATLAS_BASE_URL}/measurements"
RIPE_ATLAS_MEASUREMENTS_RESULTS_URL = f"{RIPE_ATLAS_BASE_URL}/measurements/{{measurement_id}}/results"
RIPE_ATLAS_API_KEY = os.getenv("RIPE_ATLAS_API_KEY", "")

class RIPEAtlasProvider:
    def __init__(self, api_key: str = RIPE_ATLAS_API_KEY):
        self._api_key = api_key

    @staticmethod
    def _to_api_datetime(dt: datetime) -> str:
        return dt.astimezone(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    def _auth_headers(self, require_api_key: bool = False) -> dict[str, str]:
        if not self._api_key:
            if require_api_key:
                raise ValueError("RIPE Atlas API key is required for this operation.")
            return {}
        return {"Authorization": f"Key {self._api_key}"}

    def _request(self, method: str, url: str, **kwargs) -> dict | list:
        response = requests.request(method=method, url=url, timeout=30, **kwargs)
        response.raise_for_status()
        return response.json()

    def get_probe_location_info(self, probe_id: int) -> tuple[str, float, float]:
        """
        :param probe_id: id of the probe we want the info
        :return: (country_code, latitude, longitude)
        """

        country_code = ""
        latitude = 0.0
        longitude = 0.0

        try:
            probe_info = self._request(
                method="GET",
                url=f"{RIPE_ATLAS_PROBES_URL}/{probe_id}"
            )

            country_code = probe_info["country_code"]
            latitude = probe_info["geometry"]["coordinates"][1]
            longitude = probe_info["geometry"]["coordinates"][0]

        except Exception as e:
            logger.error("Exception log from: RIPEAtlasProvider.get_probe_location_info")
            logger.error(e)

        return country_code, latitude, longitude
    
    def get_measurement_results(
            self,
            measurement_id: int) -> list[dict]:

        measurement_results_response = []
        try:
            measurement_results_response = self._request(
                method="GET",
                url=RIPE_ATLAS_MEASUREMENTS_RESULTS_URL.format(
                    measurement_id=measurement_id
                ),
                headers=self._auth_headers()
            )

            logger.debug("Log from: RIPEAtlasProvider.get_measurement_results")
            logger.debug(f"Measurements length {len(measurement_results_response)}")
        except requests.HTTPError as error:
            logger.error("Exception log from: RIPEAtlasProvider.get_measurement_results")
            logger.error(measurement_results_response)
            logger.error(error)

        return measurement_results_response
        
    def get_traceroutes_measurements_for_ip(
            self,
            target_ip: str) -> list[str]:
        """
        :param target_ip: target IP address of the measurements
        :return: list of measurement IDs
        """

        measurement_ids = []
        page = 1
        while True:
            url = f"{RIPE_ATLAS_MEASUREMENTS_URL}?target={target_ip}&" + \
                f"type=traceroute&status=Stopped&fields=description&page_size=500&page={page}"
            try:
                measurements_response = self._request(
                    method="GET",
                    url=url,
                )

                measurement_ids = [
                    m["id"] for m in measurements_response.get("results", [])
                    if "Hunter" not in m.get("description")
                ]

                logger.debug("Log from: RIPEAtlasProvider.get_measurements_for_ip")
                logger.debug(f"Measurement IDs: {measurement_ids}")

                if int(measurements_response.get("count")) > page * 500:
                    page += 1
                else:
                    break
            except requests.HTTPError as error:
                logger.error("Exception log from: RIPEAtlasProvider.get_measurements_for_ip")
                logger.error(error)
                break

        return measurement_ids

    def get_countries_with_min_active_probes(self, min_probes: int = 10) -> list[str]:
        """
        Returns ISO country codes that have at least `min_probes` active public probes.
        """

        page = 1
        country_counter: Counter[str] = Counter()

        while True:
            response = self._request(
                method="GET",
                url=RIPE_ATLAS_PROBES_URL,
                params={
                    "status": 1,
                    "is_public": "true",
                    "fields": "country_code",
                    "page_size": 500,
                    "page": page,
                },
            )

            for probe in response.get("results", []):
                country_code = probe.get("country_code")
                if country_code:
                    country_counter[country_code] += 1

            if response.get("next"):
                page += 1
                continue
            break

        countries = sorted([
            cc for cc, amount in country_counter.items() if amount >= min_probes
        ])

        logger.info(
            "Log from: RIPEAtlasProvider.get_countries_with_min_active_probes - countries=%s",
            len(countries),
        )
        return countries

    @staticmethod
    def _build_http_definition(target_url: str, interval_seconds: int, description: str) -> dict:
        parsed = urlparse(target_url)
        if parsed.scheme not in {"http", "https"}:
            raise ValueError("target_url must start with http:// or https://")
        if not parsed.hostname:
            raise ValueError("target_url must include a valid host")

        port = parsed.port or (443 if parsed.scheme == "https" else 80)
        path = parsed.path or "/"
        if parsed.query:
            path = f"{path}?{parsed.query}"

        return {
            "target": parsed.hostname,
            "description": description,
            "type": "http",
            "af": 4,
            "is_oneoff": False,
            "interval": interval_seconds,
            "method": "GET",
            "protocol": parsed.scheme.upper(),
            "port": port,
            "path": path,
            "resolve_on_probe": True,
        }

    def create_http_measurement_for_country(
            self,
            target_url: str,
            country_code: str,
            probes_requested: int = 10,
            interval_seconds: int = 21600,
            duration_days: int = 7,
            description_prefix: str = "RCA-DNS HTTP",
    ) -> dict:
        """
        Creates a recurring RIPE Atlas HTTP measurement for one country.
        Defaults: 10 probes, every 6h, during 7 days.
        """

        now = datetime.now(timezone.utc)
        stop_time = now + timedelta(days=duration_days)
        description = f"{description_prefix} [{country_code}]"

        payload = {
            "definitions": [
                self._build_http_definition(
                    target_url=target_url,
                    interval_seconds=interval_seconds,
                    description=description,
                )
            ],
            "probes": [
                {
                    "type": "country",
                    "value": country_code.upper(),
                    "requested": probes_requested,
                }
            ],
            "is_oneoff": False,
            "start_time": self._to_api_datetime(now),
            "stop_time": self._to_api_datetime(stop_time),
        }

        response = self._request(
            method="POST",
            url=RIPE_ATLAS_MEASUREMENTS_URL,
            headers={
                "Content-Type": "application/json",
                **self._auth_headers(require_api_key=True),
            },
            json=payload,
        )

        return response

    def create_global_http_measurements(
            self,
            target_url: str,
            probes_per_country: int = 10,
            interval_seconds: int = 21600,
            duration_days: int = 7,
            countries: list[str] | None = None,
            excluded_countries: list[str] | None = None,
            description_prefix: str = "RCA-DNS HTTP",
            dry_run: bool = False,
    ) -> list[dict]:
        """
        Creates one HTTP measurement per country.
        If `countries` is None, countries are auto-discovered from active probes.
        """

        if countries is None:
            countries = self.get_countries_with_min_active_probes(min_probes=probes_per_country)

        excluded = {country.upper() for country in (excluded_countries or [])}
        selected_countries = [country.upper() for country in countries if country.upper() not in excluded]
        selected_countries = sorted(set(selected_countries))

        logger.info(
            "Log from: RIPEAtlasProvider.create_global_http_measurements - selected_countries=%s",
            len(selected_countries),
        )

        results: list[dict] = []
        for country_code in selected_countries:
            if dry_run:
                results.append({
                    "country_code": country_code,
                    "status": "dry_run",
                    "target_url": target_url,
                    "probes_requested": probes_per_country,
                    "interval_seconds": interval_seconds,
                    "duration_days": duration_days,
                })
                continue

            try:
                response = self.create_http_measurement_for_country(
                    target_url=target_url,
                    country_code=country_code,
                    probes_requested=probes_per_country,
                    interval_seconds=interval_seconds,
                    duration_days=duration_days,
                    description_prefix=description_prefix,
                )
                results.append({
                    "country_code": country_code,
                    "status": "created",
                    "response": response,
                })
            except Exception as error:
                logger.error(
                    "Exception log from: RIPEAtlasProvider.create_global_http_measurements country=%s",
                    country_code,
                )
                logger.error(error)
                results.append({
                    "country_code": country_code,
                    "status": "error",
                    "error": str(error),
                })

        return results
