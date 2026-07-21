#!/bin/bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
	echo "Usage: $0 <backup_folder>" >&2
	exit 1
fi

if ! command -v rsync >/dev/null 2>&1; then
	echo "[ERROR] rsync is required but not installed" >&2
	exit 1
fi

backup_folder="$1"
project_root="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ ! -d "$backup_folder" ]]; then
	echo "[ERROR] Backup folder does not exist: $backup_folder" >&2
	exit 1
fi

# Restore every .env file found in the backup, preserving relative paths.
rsync -avm \
	--include='*/' \
	--include='.env' \
	--exclude='*' \
	"$backup_folder/" "$project_root/"

# Restore all campaign data if present in backup.
if [[ -d "$backup_folder/evaluation/data" ]]; then
	rsync -av "$backup_folder/evaluation/data/" "$project_root/evaluation/data/"
else
	echo "[WARN] No evaluation/data found in backup folder: $backup_folder" >&2
fi

echo "Restore completed from: $backup_folder"
