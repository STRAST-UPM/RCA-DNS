#!/bin/bash
set -e

###############################################################################
# Main
###############################################################################

delete_services_main() {
    log "Project: $PROJECT_ID"
    gcloud config set project "$PROJECT_ID"

    for region in "${REGIONS[@]}"; do
        delete_neg "$region"
        delete_cloud_run_service "$region"
    done
}
