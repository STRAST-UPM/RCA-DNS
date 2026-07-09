#!/bin/bash

###############################################################################
# Logging
###############################################################################

log() {
    echo "[INFO] $*"
}

warn() {
    echo "[WARNING] $*" >&2
}

error() {
    echo "[ERROR] $*" >&2
}

abort() {
    error "$@"
    exit 1
}

###############################################################################
# Generic execution helpers
###############################################################################

run_if_missing() {

    local description="$1"
    local check_command="$2"
    local create_command="$3"

    if eval "$check_command" >/dev/null 2>&1; then
        log "$description already exists."
        return 0
    fi

    log "Creating $description..."
    eval "$create_command"
}

run_if_exists() {

    local description="$1"
    local check_command="$2"
    local delete_command="$3"

    if ! eval "$check_command" >/dev/null 2>&1; then
        log "$description does not exist."
        return 0
    fi

    log "Deleting $description..."
    eval "$delete_command"
}

###############################################################################
# Resource naming
###############################################################################

sanitize() {
    echo "$1" | tr '.' '-'
}

service_name() {
    local region="$1"
    echo "${region}-service"
}

neg_name() {
    local region="$1"
    echo "${PREFIX}-$(service_name "$region")-neg"
}

backend_name() {
    local domain="$1"
    echo "${PREFIX}-backend-$(sanitize "$domain")"
}

urlmap_name() {
    local domain="$1"
    echo "${PREFIX}-urlmap-$(sanitize "$domain")"
}

certificate_name() {
    local domain="$1"
    echo "${PREFIX}-cert-$(sanitize "$domain")"
}

http_proxy_name() {
    local domain="$1"
    echo "${PREFIX}-http-proxy-$(sanitize "$domain")"
}

https_proxy_name() {
    local domain="$1"
    echo "${PREFIX}-https-proxy-$(sanitize "$domain")"
}

http_forwarding_rule_name() {
    local domain="$1"
    echo "${PREFIX}-http-rule-$(sanitize "$domain")"
}

https_forwarding_rule_name() {
    local domain="$1"
    echo "${PREFIX}-https-rule-$(sanitize "$domain")"
}

###############################################################################
# Cloud Run
###############################################################################

create_cloud_run_service() {

    local region="$1"

    local service
    service=$(service_name "$region")

    run_if_missing \
        "Cloud Run service '$service'" \
        "gcloud run services describe \
            '$service' \
            --region='$region' \
            --platform=managed \
            --project='$PROJECT_ID'" \
        "gcloud run deploy \
            '$service' \
            --image='$IMAGE' \
            --region='$region' \
            --platform=managed \
            --allow-unauthenticated \
            --project='$PROJECT_ID' \
            --set-env-vars='REGION=$region'"

    sleep "$WAIT_SECONDS"
}

delete_cloud_run_service() {

    local region="$1"

    local service
    service=$(service_name "$region")

    run_if_exists \
        "Cloud Run service '$service'" \
        "gcloud run services describe \
            '$service' \
            --region='$region' \
            --platform=managed \
            --project='$PROJECT_ID'" \
        "gcloud run services delete \
            '$service' \
            --region='$region' \
            --platform=managed \
            --project='$PROJECT_ID' \
            --quiet"
}

###############################################################################
# Serverless Network Endpoint Groups (NEGs)
###############################################################################

create_neg() {

    local region="$1"

    local neg
    local service

    neg=$(neg_name "$region")
    service=$(service_name "$region")

    run_if_missing \
        "Serverless NEG '$neg'" \
        "gcloud compute network-endpoint-groups describe \
            '$neg' \
            --region='$region' \
            --project='$PROJECT_ID'" \
        "gcloud compute network-endpoint-groups create \
            '$neg' \
            --region='$region' \
            --network-endpoint-type=serverless \
            --cloud-run-service='$service' \
            --project='$PROJECT_ID'"
}

delete_neg() {

    local region="$1"

    local neg

    neg=$(neg_name "$region")

    run_if_exists \
        "Serverless NEG '$neg'" \
        "gcloud compute network-endpoint-groups describe \
            '$neg' \
            --region='$region' \
            --project='$PROJECT_ID'" \
        "gcloud compute network-endpoint-groups delete \
            '$neg' \
            --region='$region' \
            --project='$PROJECT_ID' \
            --quiet"
}

###############################################################################
# Backend Services
###############################################################################

create_backend() {

    local domain="$1"

    local backend

    backend=$(backend_name "$domain")

    run_if_missing \
        "Backend '$backend'" \
        "gcloud compute backend-services describe \
            '$backend' \
            --global \
            --project='$PROJECT_ID'" \
        "gcloud compute backend-services create \
            '$backend' \
            --global \
            --protocol=HTTP \
            --load-balancing-scheme=EXTERNAL_MANAGED \
            --project='$PROJECT_ID'"
}

delete_backend() {

    local domain="$1"

    local backend

    backend=$(backend_name "$domain")

    run_if_exists \
        "Backend '$backend'" \
        "gcloud compute backend-services describe \
            '$backend' \
            --global \
            --project='$PROJECT_ID'" \
        "gcloud compute backend-services delete \
            '$backend' \
            --global \
            --project='$PROJECT_ID' \
            --quiet"
}

add_backend_region() {

    local domain="$1"
    local region="$2"

    local backend
    local neg

    backend=$(backend_name "$domain")
    neg=$(neg_name "$region")

    log "Adding region '$region' to backend '$backend'"

    gcloud compute backend-services add-backend \
        "$backend" \
        --global \
        --network-endpoint-group="$neg" \
        --network-endpoint-group-region="$region" \
        --project="$PROJECT_ID"
}

remove_backend_region() {

    local domain="$1"
    local region="$2"

    local backend
    local neg

    backend=$(backend_name "$domain")
    neg=$(neg_name "$region")

    log "Removing region '$region' from backend '$backend'"

    gcloud compute backend-services remove-backend \
        "$backend" \
        --global \
        --network-endpoint-group="$neg" \
        --network-endpoint-group-region="$region" \
        --project="$PROJECT_ID"
}

###############################################################################
# URL Maps
###############################################################################

create_url_map() {

    local domain="$1"

    local urlmap
    local backend

    urlmap=$(urlmap_name "$domain")
    backend=$(backend_name "$domain")

    run_if_missing \
        "URL Map '$urlmap'" \
        "gcloud compute url-maps describe \
            '$urlmap' \
            --project='$PROJECT_ID'" \
        "gcloud compute url-maps create \
            '$urlmap' \
            --default-service='$backend' \
            --project='$PROJECT_ID'"
}

delete_url_map() {

    local domain="$1"

    local urlmap

    urlmap=$(urlmap_name "$domain")

    run_if_exists \
        "URL Map '$urlmap'" \
        "gcloud compute url-maps describe \
            '$urlmap' \
            --project='$PROJECT_ID'" \
        "gcloud compute url-maps delete \
            '$urlmap' \
            --project='$PROJECT_ID' \
            --quiet"
}

###############################################################################
# SSL Certificates
###############################################################################

create_ssl_certificate() {

    local domain="$1"

    local certificate

    certificate=$(certificate_name "$domain")

    run_if_missing \
        "SSL Certificate '$certificate'" \
        "gcloud compute ssl-certificates describe \
            '$certificate' \
            --project='$PROJECT_ID'" \
        "gcloud compute ssl-certificates create \
            '$certificate' \
            --domains='$domain' \
            --project='$PROJECT_ID'"
}

delete_ssl_certificate() {

    local domain="$1"

    local certificate

    certificate=$(certificate_name "$domain")

    run_if_exists \
        "SSL Certificate '$certificate'" \
        "gcloud compute ssl-certificates describe \
            '$certificate' \
            --project='$PROJECT_ID'" \
        "gcloud compute ssl-certificates delete \
            '$certificate' \
            --project='$PROJECT_ID' \
            --quiet"
}

###############################################################################
# HTTP Proxy
###############################################################################

create_http_proxy() {

    local domain="$1"

    local proxy
    local urlmap

    proxy=$(http_proxy_name "$domain")
    urlmap=$(urlmap_name "$domain")

    run_if_missing \
        "HTTP Proxy '$proxy'" \
        "gcloud compute target-http-proxies describe \
            '$proxy' \
            --project='$PROJECT_ID'" \
        "gcloud compute target-http-proxies create \
            '$proxy' \
            --url-map='$urlmap' \
            --project='$PROJECT_ID'"
}

delete_http_proxy() {

    local domain="$1"

    local proxy

    proxy=$(http_proxy_name "$domain")

    run_if_exists \
        "HTTP Proxy '$proxy'" \
        "gcloud compute target-http-proxies describe \
            '$proxy' \
            --project='$PROJECT_ID'" \
        "gcloud compute target-http-proxies delete \
            '$proxy' \
            --project='$PROJECT_ID' \
            --quiet"
}

###############################################################################
# HTTPS Proxy
###############################################################################

create_https_proxy() {

    local domain="$1"

    local proxy
    local urlmap
    local certificate

    proxy=$(https_proxy_name "$domain")
    urlmap=$(urlmap_name "$domain")
    certificate=$(certificate_name "$domain")

    run_if_missing \
        "HTTPS Proxy '$proxy'" \
        "gcloud compute target-https-proxies describe \
            '$proxy' \
            --project='$PROJECT_ID'" \
        "gcloud compute target-https-proxies create \
            '$proxy' \
            --url-map='$urlmap' \
            --ssl-certificates='$certificate' \
            --project='$PROJECT_ID'"
}

delete_https_proxy() {

    local domain="$1"

    local proxy

    proxy=$(https_proxy_name "$domain")

    run_if_exists \
        "HTTPS Proxy '$proxy'" \
        "gcloud compute target-https-proxies describe \
            '$proxy' \
            --project='$PROJECT_ID'" \
        "gcloud compute target-https-proxies delete \
            '$proxy' \
            --project='$PROJECT_ID' \
            --quiet"
}

###############################################################################
# HTTP Forwarding Rules
###############################################################################

create_http_forwarding_rule() {

    local domain="$1"

    local rule
    local proxy

    rule=$(http_forwarding_rule_name "$domain")
    proxy=$(http_proxy_name "$domain")

    run_if_missing \
        "HTTP Forwarding Rule '$rule'" \
        "gcloud compute forwarding-rules describe \
            '$rule' \
            --global \
            --project='$PROJECT_ID'" \
        "gcloud compute forwarding-rules create \
            '$rule' \
            --global \
            --target-http-proxy='$proxy' \
            --ports=80 \
            --project='$PROJECT_ID'"
}

delete_http_forwarding_rule() {

    local domain="$1"

    local rule

    rule=$(http_forwarding_rule_name "$domain")

    run_if_exists \
        "HTTP Forwarding Rule '$rule'" \
        "gcloud compute forwarding-rules describe \
            '$rule' \
            --global \
            --project='$PROJECT_ID'" \
        "gcloud compute forwarding-rules delete \
            '$rule' \
            --global \
            --project='$PROJECT_ID' \
            --quiet"
}

###############################################################################
# HTTPS Forwarding Rules
###############################################################################

create_https_forwarding_rule() {

    local domain="$1"

    local rule
    local proxy

    rule=$(https_forwarding_rule_name "$domain")
    proxy=$(https_proxy_name "$domain")

    run_if_missing \
        "HTTPS Forwarding Rule '$rule'" \
        "gcloud compute forwarding-rules describe \
            '$rule' \
            --global \
            --project='$PROJECT_ID'" \
        "gcloud compute forwarding-rules create \
            '$rule' \
            --global \
            --target-https-proxy='$proxy' \
            --ports=443 \
            --project='$PROJECT_ID'"
}

delete_https_forwarding_rule() {

    local domain="$1"

    local rule

    rule=$(https_forwarding_rule_name "$domain")

    run_if_exists \
        "HTTPS Forwarding Rule '$rule'" \
        "gcloud compute forwarding-rules describe \
            '$rule' \
            --global \
            --project='$PROJECT_ID'" \
        "gcloud compute forwarding-rules delete \
            '$rule' \
            --global \
            --project='$PROJECT_ID' \
            --quiet"
}

###############################################################################
# Information
###############################################################################

show_forwarding_rules() {

    echo
    echo "Global forwarding rules:"
    echo

    gcloud compute forwarding-rules list \
        --global \
        --format="table(NAME,IPAddress,TARGET)"
}

###############################################################################
# Domain deployment
###############################################################################

deploy_domain() {

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

delete_domain() {

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
