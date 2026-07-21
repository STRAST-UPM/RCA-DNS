# external imports
from datetime import datetime, timedelta, timezone
from ripe.atlas.cousteau import (
    Http,
    AtlasSource,
    AtlasCreateRequest
)
# internal imports
from src.utilities.utils import (
    json_file_to_list,
    dict_to_json_file
)
from src.utilities.constants import (
    RIPE_ATLAS_API_KEY,
    CAMPAIGN_NAME,
    CAMPAIGN_FOLDER_PATH,
    WORLD_COUNTRY_CODES_LIST_FILEPATH
)


class RIPEAtlasProvider:
    def __init__(self):
        self._api_key = RIPE_ATLAS_API_KEY

    def http_from_every_country(
        self,
        description: str,
        targets: list[str],
        measurement_info_filename: str,
        af: int = 4,
        # 8 hours by defaults, 3 times a day.
        interval_seconds: int = 8 * 60 * 60,
        duration_days: int = 7,
        start_time: datetime | None = None,
        
    ):
        if start_time is None:
            start_time = datetime.now(timezone.utc) + timedelta(seconds=10)

        stop_time = start_time + timedelta(days=duration_days)

        http_measurements = []
        for target in targets:
            http_measurements.append(Http(
                af=af,
                description=description,
                target=target
            ))

        probes_worldwide = []
        for country_code in json_file_to_list(WORLD_COUNTRY_CODES_LIST_FILEPATH):
            probes_worldwide.append(AtlasSource(
                type="country",
                value=country_code,
                requested=5,
            ))

        request = AtlasCreateRequest(
            key=self._api_key,
            measurements=http_measurements,
            sources=probes_worldwide,
            is_oneoff=False,
            start_time=start_time,
            stop_time=stop_time,
            interval=interval_seconds,
        )

        is_success, response = request.create()
        print(response)
        
        if not is_success:
            raise RuntimeError(f"Could not create measurements: {response}")
        
        # Save measurements ids
        ids = response.get("measurements", [])
        measurements_ids = [measurement_id for measurement_id in ids if isinstance(measurement_id, int)]

        measurements_info = {
            "start_time": start_time.isoformat(),
            "stop_time": stop_time.isoformat(),
            "measurements_ids": measurements_ids
        }

        dict_to_json_file(
            file_path=f"{CAMPAIGN_FOLDER_PATH}/{measurement_info_filename}.json",
            dict_to_save=measurements_info,
        )
