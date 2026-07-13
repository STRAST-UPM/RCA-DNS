#!/bin/bash
# shellcheck disable=SC2034
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GOOGLE_CLOUD_DIR="$(cd "$SCRIPT_DIR/../.." && pwd)"
ENV_FILE="$GOOGLE_CLOUD_DIR/.env"
GOOGLE_CLOUD_DIR_SCRIPTS="$GOOGLE_CLOUD_DIR/scripts"
LOGS_DIR="$GOOGLE_CLOUD_DIR/logs"
LOG_FILE="$LOGS_DIR/log-$(date +%Y%m%d_%H-%M-%S).log"


if [[ ! -f "$ENV_FILE" ]]; then
    echo "[ERROR] Missing env file: $ENV_FILE" >&2
    echo "Copy .env.example to .env and adjust values before running scripts." >&2
    exit 1
fi

# Load environment and export simple vars for subprocesses.
set -a
# shellcheck source=/dev/null
source "$ENV_FILE"
set +a

touch "$LOG_FILE"

# shellcheck disable=SC2034
declare -gA DOMAINS

DOMAINS["global.$BASE_DOMAIN"]="${DOMAIN_GLOBAL_REGIONS:-${REGIONS[*]}}"
DOMAINS["africa.$BASE_DOMAIN"]="${DOMAIN_AFRICA_REGIONS:-}"
DOMAINS["asia.$BASE_DOMAIN"]="${DOMAIN_ASIA_REGIONS:-}"
DOMAINS["australia.$BASE_DOMAIN"]="${DOMAIN_AUSTRALIA_REGIONS:-}"
DOMAINS["europe.$BASE_DOMAIN"]="${DOMAIN_EUROPE_REGIONS:-}"
DOMAINS["middleeast.$BASE_DOMAIN"]="${DOMAIN_MIDDLEEAST_REGIONS:-}"
DOMAINS["northamerica.$BASE_DOMAIN"]="${DOMAIN_NORTHAMERICA_REGIONS:-}"
DOMAINS["us.$BASE_DOMAIN"]="${DOMAIN_US_REGIONS:-}"
DOMAINS["southamerica.$BASE_DOMAIN"]="${DOMAIN_SOUTHAMERICA_REGIONS:-}"

bootstrap_load_scripts() {
    local file

    while IFS= read -r file; do
        # shellcheck source=/dev/null
        source "$file"
    done < <(find "$SCRIPT_DIR" -type f -name "*.sh" ! -name "bootstrap.sh" -print | sort)
}
