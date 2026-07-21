#!/bin/bash
# shellcheck disable=SC2034
set -euo pipefail

###############################################################################
# Google Cloud Run regions
###############################################################################

REGIONS_AFRICA=(
    africa-south1               # Johannesburg
)

REGIONS_NORTHAMERICA=(
    northamerica-northeast1     # Toronto
    northamerica-northeast2     # Montreal
    northamerica-south1         # Mexico
)

REGIONS_US=(
    us-central1                 # Iowa
    us-east1                    # South Carolina
    us-east4                    # Northern Virginia
    us-east5                    # Columbus
    us-south1                   # Dallas
    us-west1                    # Oregon
    us-west2                    # Los Angeles
    us-west3                    # Salt Lake City
    us-west4                    # Las Vegas
)

REGIONS_SOUTHAMERICA=(
    southamerica-east1          # São Paulo
    southamerica-west1          # Santiago
)

REGIONS_EUROPE=(
    europe-central2             # Warsaw
    europe-north1               # Finland
    europe-north2               # Stockholm
    europe-southwest1           # Madrid
    europe-west1                # Belgium
    europe-west2                # London
    europe-west3                # Frankfurt
    europe-west4                # Netherlands
    europe-west6                # Zurich
    europe-west8                # Milan
    europe-west9                # Paris
    europe-west10               # Berlin
    europe-west12               # Turin
)

REGIONS_ASIA=(
    asia-east1                  # Taiwan
    asia-east2                  # Hong Kong
    asia-northeast1             # Tokyo
    asia-northeast2             # Osaka
    asia-northeast3             # Seoul
    asia-south1                 # Mumbai
    asia-south2                 # Delhi
    asia-southeast1             # Singapore
    asia-southeast2             # Jakarta
)

REGIONS_AUSTRALIA=(
    australia-southeast1        # Sydney
    australia-southeast2        # Melbourne
)

# Some middle east regions are restricted in Google Cloud
# REGIONS_MIDDLEEAST=(
#     me-central1                 # Doha
#     me-central2                 # Dammam
#     me-west1                    # Tel Aviv
# )

REGIONS=(
    "${REGIONS_AFRICA[@]}"
    "${REGIONS_NORTHAMERICA[@]}"
    "${REGIONS_US[@]}"
    "${REGIONS_SOUTHAMERICA[@]}"
    "${REGIONS_EUROPE[@]}"
    "${REGIONS_ASIA[@]}"
    "${REGIONS_AUSTRALIA[@]}"
    # "${REGIONS_MIDDLEEAST[@]}"
)

# shellcheck disable=SC2034
declare -gA DOMAINS

DOMAINS["global.$BASE_DOMAIN"]="${REGIONS[*]}"
DOMAINS["africa.$BASE_DOMAIN"]="${REGIONS_AFRICA[*]}"
DOMAINS["asia.$BASE_DOMAIN"]="${REGIONS_ASIA[*]}"
DOMAINS["australia.$BASE_DOMAIN"]="${REGIONS_AUSTRALIA[*]}"
DOMAINS["europe.$BASE_DOMAIN"]="${REGIONS_EUROPE[*]}"
# DOMAINS["middleeast.$BASE_DOMAIN"]="${REGIONS_MIDDLEEAST[*]}"
DOMAINS["northamerica.$BASE_DOMAIN"]="${REGIONS_NORTHAMERICA[*]}"
DOMAINS["us.$BASE_DOMAIN"]="${REGIONS_US[*]}"
DOMAINS["southamerica.$BASE_DOMAIN"]="${REGIONS_SOUTHAMERICA[*]}"


# Paths constants
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
ROOT_ENV_FILE="$PROJECT_ROOT/.env"
DEPLOYMENT_DIR="$PROJECT_ROOT/deployment"
GOOGLE_CLOUD_DIR="$DEPLOYMENT_DIR/GoogleCloud"
ENV_FILE="$GOOGLE_CLOUD_DIR/.env"
SCRIPTS_DIR="$GOOGLE_CLOUD_DIR/scripts"

LOGS_DIR="$GOOGLE_CLOUD_DIR/logs"
LOG_FILE="$LOGS_DIR/log-$(date +%Y%m%d_%H-%M-%S).log"

STATICS_DIR="$GOOGLE_CLOUD_DIR/statics"
HELP_TEXT_FILETPATH="$STATICS_DIR/help.txt"

###############################################################################

if [[ ! -f "$ROOT_ENV_FILE" && ! -f "$DEPLOYMENT_ENV_FILE" ]]; then
    echo "[ERROR] Missing env files." >&2
    echo "Expected at least one of:" >&2
    echo "  - $ROOT_ENV_FILE" >&2
    echo "  - $DEPLOYMENT_ENV_FILE" >&2
    exit 1
fi

# Load shared env first, then allow deployment-specific overrides.
set -a
if [[ -f "$ROOT_ENV_FILE" ]]; then
    # shellcheck source=/dev/null
    source "$ROOT_ENV_FILE"
fi
if [[ -f "$DEPLOYMENT_ENV_FILE" ]]; then
    # shellcheck source=/dev/null
    source "$DEPLOYMENT_ENV_FILE"
fi
set +a

touch "$LOG_FILE"

# Capture all output from this shell (including external tools) to screen and log.
exec > >(tee -a "$LOG_FILE") 2>&1



bootstrap_load_scripts() {
    local file

    while IFS= read -r file; do
        # shellcheck source=/dev/null
        source "$file"
    done < <(find "$SCRIPT_DIR" -type f -name "*.sh" ! -name "bootstrap.sh" -print | sort)
}
