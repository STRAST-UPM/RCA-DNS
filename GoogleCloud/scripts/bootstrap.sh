#!/bin/bash
# shellcheck disable=SC2034
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ENV_FILE="$ROOT_DIR/.env"

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

# shellcheck disable=SC2034
declare -gA DOMAINS

DOMAINS["global.anycastprivacy.org"]="${DOMAIN_GLOBAL_REGIONS:-${REGIONS[*]}}"
DOMAINS["africa.anycastprivacy.org"]="${DOMAIN_AFRICA_REGIONS:-}"
DOMAINS["asia.anycastprivacy.org"]="${DOMAIN_ASIA_REGIONS:-}"
DOMAINS["australia.anycastprivacy.org"]="${DOMAIN_AUSTRALIA_REGIONS:-}"
DOMAINS["europe.anycastprivacy.org"]="${DOMAIN_EUROPE_REGIONS:-}"
DOMAINS["middleeast.anycastprivacy.org"]="${DOMAIN_MIDDLEEAST_REGIONS:-}"
DOMAINS["northamerica.anycastprivacy.org"]="${DOMAIN_NORTHAMERICA_REGIONS:-}"
DOMAINS["us.anycastprivacy.org"]="${DOMAIN_US_REGIONS:-}"
DOMAINS["southamerica.anycastprivacy.org"]="${DOMAIN_SOUTHAMERICA_REGIONS:-}"

bootstrap_load_scripts() {
    local file

    while IFS= read -r file; do
        # shellcheck source=/dev/null
        source "$file"
    done < <(find "$SCRIPT_DIR" -type f -name "*.sh" ! -name "bootstrap.sh" -print | sort)
}
