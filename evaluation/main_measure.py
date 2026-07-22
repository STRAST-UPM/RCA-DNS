# external imports
import datetime
# internal imports
from src.providers.ripeatlas_provider import RIPEAtlasProvider
from src.utilities.constants import (
    CAMPAIGN_NAME,
    RCA_DNS_DOMAINS
)


if __name__ == "__main__":
    ripe_atlas_provider = RIPEAtlasProvider()
    measurement_info_filename = \
        f"{datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%SZ')}_{CAMPAIGN_NAME}_measurements_info"
    ripe_atlas_provider.http_from_every_country(
        description=f"HTTP measurement for RCA-DNS validation",
        targets=list(RCA_DNS_DOMAINS.keys()),
        duration_days=7,
        interval_seconds=8*60*60,
        measurement_info_filename=measurement_info_filename
    )
