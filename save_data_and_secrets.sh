#!/bin/bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
	echo "Usage: $0 <destination_folder>" >&2
	exit 1
fi

if ! command -v rsync >/dev/null 2>&1; then
	echo "[ERROR] rsync is required but not installed" >&2
	exit 1
fi

destination_folder="$1"
project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$destination_folder"

# Copy every .env file in the repository, preserving relative paths.
rsync -avm \
	--include='*/' \
	--include='.env' \
	--exclude='*' \
	"$project_root/" "$destination_folder/"

# Copy all campaign data.
if [[ -d "$project_root/evaluation/data" ]]; then
	rsync -av "$project_root/evaluation/data/" "$destination_folder/evaluation/data/"
fi

echo "Backup completed in: $destination_folder"
