#!/bin/bash
set -e

###############################################################################
# Main
###############################################################################

delete_services_main() {
    echo "Project: $PROJECT_ID"
    echo

    for region in "${REGIONS[@]}"; do
        delete_neg "$region"
        delete_cloud_run_service "$region"
    done    
}
