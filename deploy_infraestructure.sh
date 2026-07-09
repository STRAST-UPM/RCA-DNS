#!/bin/bash
set -e

source config.sh
source lib.sh

echo "Project: $PROJECT_ID"
echo

for domain in "${!DOMAINS[@]}"; do
    deploy_domain "$domain"
done

echo
show_forwarding_rules
