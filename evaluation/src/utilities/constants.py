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
BASE_DOMAIN = getenv("BASE_DOMAIN","")

################################################################################

# Paths constants
__EVALUATION_FOLDER_PATH = f"{__PROJECT_ROOT__}/evaluation"
__DATA_FOLDER_PATH = f"{__EVALUATION_FOLDER_PATH}/data"
__SRC_FOLDER_PATH = f"{__EVALUATION_FOLDER_PATH}/src"
__RESOURCES_FOLDER_PATH = f"{__SRC_FOLDER_PATH}/resources"

## Data paths
CAMPAIGN_FOLDER_PATH = f"{__DATA_FOLDER_PATH}/{CAMPAIGN_NAME}"
CAMPAIGN_RESULTS_RESUME_FILEPATH = f"{CAMPAIGN_FOLDER_PATH}/results_resume.csv"
CAMPAIGN_RESULTS_FOLDER_PATH = f"{CAMPAIGN_FOLDER_PATH}/results"
CAMPAIGN_ANALYSIS_REPORT_FILEPATH = f"{CAMPAIGN_FOLDER_PATH}/analysis_report.json"
CAMPAIGN_GRAPHICS_FOLDER_PATH = f"{CAMPAIGN_FOLDER_PATH}/graphics"

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

################################################################################

# RCA-DNS
RCA_DNS_DOMAINS={
    f"global.{BASE_DOMAIN}": "136.69.74.5",
    f"africa.{BASE_DOMAIN}": "136.69.107.84",
    f"asia.{BASE_DOMAIN}": "34.50.157.186",
    f"australia.{BASE_DOMAIN}": "136.68.142.0",
    f"europe.{BASE_DOMAIN}": "8.232.14.99",
    f"northamerica.{BASE_DOMAIN}": "8.232.205.19",
    f"us.{BASE_DOMAIN}": "136.68.198.50",
    f"southamerica.{BASE_DOMAIN}": "136.69.55.215",
}

RCA_DNS_IPS={
    "136.69.74.5": f"global.{BASE_DOMAIN}",
    "136.69.107.84": f"africa.{BASE_DOMAIN}",
    "34.50.157.186": f"asia.{BASE_DOMAIN}",
    "136.68.142.0": f"australia.{BASE_DOMAIN}",
    "8.232.14.99": f"europe.{BASE_DOMAIN}",
    "8.232.205.19": f"northamerica.{BASE_DOMAIN}",
    "136.68.198.50": f"us.{BASE_DOMAIN}",
    "136.69.55.215": f"southamerica.{BASE_DOMAIN}",
}

# 100ms is the mark of good time response
GOOD_RESPONSE_TIME_LIMIT_MS = 100
MID_RESPONSE_TIME_LIMIT_MS = 150