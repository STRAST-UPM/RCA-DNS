#!/bin/bash
set -e

###############################################################################
# Delete Functions
###############################################################################

delete_domain_infraestructure() {

    local domain="$1"

    log "Deleting infrastructure for '$domain'"

    # Uncomment if HTTPS is enabled
    # delete_https_forwarding_rule "$domain"
    # delete_https_proxy "$domain"
    # delete_ssl_certificate "$domain"

    delete_http_forwarding_rule "$domain"
    delete_http_proxy "$domain"

    delete_url_map "$domain"

    for region in ${DOMAINS[$domain]}; do
        remove_backend_region "$domain" "$region"
    done

    delete_backend "$domain"
}

###############################################################################
# Main
###############################################################################

delete_infraestructure_main() {
    echo "Project: $PROJECT_ID"
    echo

    for domain in "${!DOMAINS[@]}"; do
        delete_domain_infraestructure "$domain"
    done
}


