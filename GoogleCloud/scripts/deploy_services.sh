#!/bin/bash
set -e

###############################################################################
# Execution
###############################################################################

echo "Project: $PROJECT_ID"
echo

for region in "${REGIONS[@]}"; do
    create_cloud_run_service "$region"
done
