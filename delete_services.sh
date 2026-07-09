#!/bin/bash
set -e

source config.sh
source lib.sh

echo "Project: $PROJECT_ID"
echo

for region in "${REGIONS[@]}"; do
    delete_neg "$region"
    delete_cloud_run_service "$region"
done
