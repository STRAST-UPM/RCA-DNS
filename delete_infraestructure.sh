#!/bin/bash
set -e

source config.sh
source lib.sh

echo "Project: $PROJECT_ID"
echo

for domain in "${!DOMAINS[@]}"; do
    delete_domain "$domain"
done
