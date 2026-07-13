#!/bin/bash
set -e

###############################################################################
# Deployment Functions
###############################################################################

deploy_domain_infraestructure() {

    local domain="$1"

    log "Deploying infrastructure for '$domain'"

    create_backend "$domain"

    for region in ${DOMAINS[$domain]}; do
        create_neg "$region"
        add_backend_region "$domain" "$region"
    done

    create_url_map "$domain"

    # Uncomment if HTTPS is required
    # create_ssl_certificate "$domain"
    # create_https_proxy "$domain"
    # create_https_forwarding_rule "$domain"

    create_http_proxy "$domain"
    create_http_forwarding_rule "$domain"
}

###############################################################################
# Main
###############################################################################

deploy_infraestructure_main() {
    log "Project: $PROJECT_ID"
    gcloud config set project "$PROJECT_ID"

    for domain in "${!DOMAINS[@]}"; do
        deploy_domain_infraestructure "$domain"
    done

    show_forwarding_rules
}
