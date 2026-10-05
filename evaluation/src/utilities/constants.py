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
CAMPAIGN_ORDERED_MEASUREMENTS_INFO_SUFIX = "measurements_info"
CAMPAIGN_RESULTS_RESUME_FILEPATH = f"{CAMPAIGN_FOLDER_PATH}/results_resume.csv"
CAMPAIGN_ANALYSIS_REPORT_FILEPATH = f"{CAMPAIGN_FOLDER_PATH}/analysis_report.json"
CAMPAIGN_PROBES_INFO_FILEPATH = f"{CAMPAIGN_FOLDER_PATH}/probes_info.json"
CAMPAIGN_RESULTS_FOLDER_PATH = f"{CAMPAIGN_FOLDER_PATH}/results"
CAMPAIGN_GRAPHICS_FOLDER_PATH = f"{CAMPAIGN_FOLDER_PATH}/graphics"

################################################################################

### Resources paths
WORLD_COUNTRIES_INFO_DICT_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/world_countries_info_dict.json"
WORLD_COUNTRIES_INFO_LIST_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/world_countries_info_list.json"
WORLD_COUNTRY_CODES_LIST_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/world_country_codes_list.json"
AFRICA_COUNTRY_CODES_LIST_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/africa_country_codes_list.json"
AMERICA_COUNTRY_CODES_LIST_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/america_country_codes_list.json"
NORTHAMERICA_COUNTRY_CODES_LIST_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/northamerica_country_codes_list.json"
SOUTHAMERICA_COUNTRY_CODES_LIST_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/southamerica_country_codes_list.json"
ASIA_COUNTRY_CODES_LIST_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/asia_country_codes_list.json"
EUROPE_COUNTRY_CODES_LIST_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/europe_country_codes_list.json"
EEA_EXTENDED_COUNTRY_CODES_LIST_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/eea_extended_country_codes_list.json"
OCEANIA_COUNTRY_CODES_LIST_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/oceania_country_codes_list.json"
VERLOC_NUMERIC_APPROXIMATION_FILEPATH = f"{__RESOURCES_FOLDER_PATH}/verloc_distance_approximation.json"

################################################################################

# RCA-DNS
RCA_DNS_DOMAINS={
    f"global.{BASE_DOMAIN}": "136.69.74.5",
    f"africa.{BASE_DOMAIN}": "136.69.107.84",
    f"asia.{BASE_DOMAIN}": "34.50.157.186",
    f"australia.{BASE_DOMAIN}": "136.68.142.0",
    f"eea-extended.{BASE_DOMAIN}": "8.232.14.99",
    f"northamerica.{BASE_DOMAIN}": "8.232.205.19",
    f"us.{BASE_DOMAIN}": "136.68.198.50",
    f"southamerica.{BASE_DOMAIN}": "136.69.55.215",
}

RCA_DNS_IPS={
    "136.69.74.5": f"global.{BASE_DOMAIN}",
    "136.69.107.84": f"africa.{BASE_DOMAIN}",
    "34.50.157.186": f"asia.{BASE_DOMAIN}",
    "136.68.142.0": f"australia.{BASE_DOMAIN}",
    "8.232.14.99": f"eea-extended.{BASE_DOMAIN}",
    "8.232.205.19": f"northamerica.{BASE_DOMAIN}",
    "136.68.198.50": f"us.{BASE_DOMAIN}",
    "136.69.55.215": f"southamerica.{BASE_DOMAIN}",
}

# 100ms is the mark of good time response
GOOD_RESPONSE_TIME_LIMIT_MS = 100
MID_RESPONSE_TIME_LIMIT_MS = 150


################################################################################
# Google Cloud locations used in the RCA-DNS prototype
# (mirrors deployment/GoogleCloud/scripts/bootstrap.sh)
# Coordinates are approximate city-level positions of each Google Cloud region.

GC_LOCATIONS = {
    # Africa
    "africa-south1":            {"city": "Johannesburg",   "lat": -26.20, "lon":   28.05},
    # North America (Canada and Mexico)
    "northamerica-northeast1":  {"city": "Montreal",       "lat":  45.50, "lon":  -73.57},
    "northamerica-northeast2":  {"city": "Toronto",        "lat":  43.65, "lon":  -79.38},
    "northamerica-south1":      {"city": "Queretaro",      "lat":  20.59, "lon": -100.39},
    # United States
    "us-central1":              {"city": "Iowa",           "lat":  41.26, "lon":  -95.86},
    "us-east1":                 {"city": "South Carolina", "lat":  33.20, "lon":  -80.01},
    "us-east4":                 {"city": "N. Virginia",    "lat":  39.04, "lon":  -77.49},
    "us-east5":                 {"city": "Columbus",       "lat":  39.96, "lon":  -83.00},
    "us-south1":                {"city": "Dallas",         "lat":  32.78, "lon":  -96.80},
    "us-west1":                 {"city": "Oregon",         "lat":  45.60, "lon": -121.18},
    "us-west2":                 {"city": "Los Angeles",    "lat":  34.05, "lon": -118.24},
    "us-west3":                 {"city": "Salt Lake City", "lat":  40.76, "lon": -111.89},
    "us-west4":                 {"city": "Las Vegas",      "lat":  36.17, "lon": -115.14},
    # South America
    "southamerica-east1":       {"city": "Sao Paulo",      "lat": -23.55, "lon":  -46.63},
    "southamerica-west1":       {"city": "Santiago",       "lat": -33.45, "lon":  -70.67},
    # EEA-Extended
    "europe-central2":          {"city": "Warsaw",         "lat":  52.23, "lon":   21.01},
    "europe-north1":            {"city": "Finland",        "lat":  60.57, "lon":   27.20},
    "europe-north2":            {"city": "Stockholm",      "lat":  59.33, "lon":   18.07},
    "europe-southwest1":        {"city": "Madrid",         "lat":  40.42, "lon":   -3.70},
    "europe-west1":             {"city": "Belgium",        "lat":  50.45, "lon":    3.82},
    "europe-west2":             {"city": "London",         "lat":  51.51, "lon":   -0.13},
    "europe-west3":             {"city": "Frankfurt",      "lat":  50.11, "lon":    8.68},
    "europe-west4":             {"city": "Netherlands",    "lat":  53.44, "lon":    6.83},
    "europe-west6":             {"city": "Zurich",         "lat":  47.38, "lon":    8.54},
    "europe-west8":             {"city": "Milan",          "lat":  45.46, "lon":    9.19},
    "europe-west9":             {"city": "Paris",          "lat":  48.86, "lon":    2.35},
    "europe-west10":            {"city": "Berlin",         "lat":  52.52, "lon":   13.40},
    "europe-west12":            {"city": "Turin",          "lat":  45.07, "lon":    7.69},
    # Asia
    "asia-east1":               {"city": "Taiwan",         "lat":  24.05, "lon":  120.52},
    "asia-east2":               {"city": "Hong Kong",      "lat":  22.32, "lon":  114.17},
    "asia-northeast1":          {"city": "Tokyo",          "lat":  35.68, "lon":  139.69},
    "asia-northeast2":          {"city": "Osaka",          "lat":  34.69, "lon":  135.50},
    "asia-northeast3":          {"city": "Seoul",          "lat":  37.57, "lon":  126.98},
    "asia-south1":              {"city": "Mumbai",         "lat":  19.08, "lon":   72.88},
    "asia-south2":              {"city": "Delhi",          "lat":  28.61, "lon":   77.21},
    "asia-southeast1":          {"city": "Singapore",      "lat":   1.35, "lon":  103.82},
    "asia-southeast2":          {"city": "Jakarta",        "lat":  -6.21, "lon":  106.85},
    # Australia
    "australia-southeast1":     {"city": "Sydney",         "lat": -33.87, "lon":  151.21},
    "australia-southeast2":     {"city": "Melbourne",      "lat": -37.81, "lon":  144.96},
}

# Regional deployments (same grouping as DOMAINS in bootstrap.sh)
GC_LOCATIONS_BY_REGION = {
    "eea-extended": [
        "europe-central2", "europe-north1", "europe-north2", "europe-southwest1",
        "europe-west1", "europe-west2", "europe-west3", "europe-west4",
        "europe-west6", "europe-west8", "europe-west9", "europe-west10",
        "europe-west12",
    ],
    "us": [
        "us-central1", "us-east1", "us-east4", "us-east5", "us-south1",
        "us-west1", "us-west2", "us-west3", "us-west4",
    ],
    "northamerica": [
        "northamerica-northeast1", "northamerica-northeast2", "northamerica-south1",
    ],
    "southamerica": ["southamerica-east1", "southamerica-west1"],
    "asia": [
        "asia-east1", "asia-east2", "asia-northeast1", "asia-northeast2",
        "asia-northeast3", "asia-south1", "asia-south2", "asia-southeast1",
        "asia-southeast2",
    ],
    "australia": ["australia-southeast1", "australia-southeast2"],
    "africa": ["africa-south1"],
}

# One colour per regional deployment (colour-blind friendly palette, Okabe-Ito)
RCA_DNS_REGION_COLORS = {
    "eea-extended": "#0072B2",
    "us":           "#D55E00",
    "northamerica": "#E69F00",
    "southamerica": "#009E73",
    "asia":         "#CC79A7",
    "australia":    "#56B4E9",
    "africa":       "#8C6D31",
}
