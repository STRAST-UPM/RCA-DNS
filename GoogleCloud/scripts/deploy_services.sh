#!/bin/bash
set -e

###############################################################################
# Main
###############################################################################

deploy_services_main() {
    echo "Project: $PROJECT_ID"
    echo

    for region in "${REGIONS[@]}"; do
        create_cloud_run_service "$region"
    done
}
