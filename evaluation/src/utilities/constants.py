# external imports
from os import (
    path, 
    getenv
)
from dotenv import load_dotenv
# internal imports

## Absolute path to the project
__PROJECT_ROOT__ = path.dirname(
    path.dirname(
        path.dirname(
            path.dirname(
                path.abspath(__file__)
            )
        )
    )
)

################################################################################
# Environment values
ENV_FILEPATH = f"{__PROJECT_ROOT__}/.env"
EVALUATION_ENV_FILEPATH = f"{__PROJECT_ROOT__}/evaluation/.env"

# Load shared variables first, then allow evaluation-specific overrides.
load_dotenv(ENV_FILEPATH)
load_dotenv(EVALUATION_ENV_FILEPATH, override=True)

RIPE_ATLAS_API_KEY = getenv("RIPE_ATLAS_API_KEY", "")
LOG_LEVEL = getenv("LOG_LEVEL", "INFO")
CAMPAIGN_NAME = getenv("CAMPAIGN_NAME", "")


################################################################################

# Paths constants
__EVALUATION_FOLDER_PATH = f"{__PROJECT_ROOT__}/evaluation"
__DATA_FOLDER_PATH = f"{__EVALUATION_FOLDER_PATH}/data"
__SRC_FOLDER_PATH = f"{__EVALUATION_FOLDER_PATH}/src"
__RESOURCES_FOLDER_PATH = f"{__SRC_FOLDER_PATH}/resources"

## Data paths
CAMPAIGN_FOLDER_PATH = f"{__DATA_FOLDER_PATH}/{CAMPAIGN_NAME}"
CAMPAIGN_RESULTS_FOLDER_PATH = f"{CAMPAIGN_FOLDER_PATH}/results"


################################################################################

### Resources paths
WORLD_COUNTRIES_INFO_DICT_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/world_countries_info_dict.json"
WORLD_COUNTRIES_INFO_LIST_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/world_countries_info_list.json"
WORLD_COUNTRY_CODES_LIST_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/world_country_codes_list.json"
AFRICA_COUNTRY_CODES_LIST_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/africa_country_codes_list.json"
AMERICA_COUNTRY_CODES_LIST_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/america_country_codes_list.json"
ASIA_COUNTRY_CODES_LIST_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/asia_country_codes_list.json"
EUROPE_COUNTRY_CODES_LIST_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/europe_country_codes_list.json"
OCEANIA_COUNTRY_CODES_LIST_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/oceania_country_codes_list.json"
VERLOC_NUMERIC_APPROXIMATION_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/verloc_distance_approximation.json"
