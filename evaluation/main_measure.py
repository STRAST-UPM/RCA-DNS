# external imports
import datetime
# internal imports
from src.providers.ripeatlas_provider import RIPEAtlasProvider
from src.utilities.constants import (
    CAMPAIGN_NAME
)


BASE_TARGET_DOMAIN="anycastprivacy.org"
TARGETS_DOMAINS=[
    f"global.{BASE_TARGET_DOMAIN}",
    # f"africa.{BASE_TARGET_DOMAIN}",
    # f"asia.{BASE_TARGET_DOMAIN}",
    # f"australia.{BASE_TARGET_DOMAIN}",
    f"europe.{BASE_TARGET_DOMAIN}",
    # f"northamerica.{BASE_TARGET_DOMAIN}",
    # f"us.{BASE_TARGET_DOMAIN}",
    # f"southamerica.{BASE_TARGET_DOMAIN}",
]


if __name__ == "__main__":
    ripe_atlas_provider = RIPEAtlasProvider()
    measurement_info_filename = \
        f"{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{CAMPAIGN_NAME}_measurements_info"
    ripe_atlas_provider.http_from_every_country(
        description=f"HTTP measurement for RCA-DNS validation",
        targets=TARGETS_DOMAINS,
        duration_days=7,
        interval_seconds=8*60*60,
        measurement_info_filename=measurement_info_filename
    )
