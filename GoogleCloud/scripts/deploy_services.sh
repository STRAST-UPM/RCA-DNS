#!/bin/bash
set -e

###############################################################################
# Main
###############################################################################

deploy_services_main() {
    log "Project: $PROJECT_ID"
    gcloud config set project "$PROJECT_ID"

    for region in "${REGIONS[@]}"; do
        create_cloud_run_service "$region"
    done
}
