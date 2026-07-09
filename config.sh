#!/bin/bash

###############################################################################
# General configuration
###############################################################################

PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
IMAGE="gcr.io/STRAST_UPM/base_service_js:latest"
PREFIX="exp"
WAIT_SECONDS=60

###############################################################################
# Google Cloud Run regions
###############################################################################

REGIONS=(
    africa-south1          # Johannesburg

    northamerica-northeast1    # Toronto
    northamerica-northeast2    # Montreal
    northamerica-south1        # Mexico

    us-central1                # Iowa
    us-east1                   # South Carolina
    us-east4                   # Northern Virginia
    us-east5                   # Columbus
    us-south1                  # Dallas
    us-west1                   # Oregon
    us-west2                   # Los Angeles
    us-west3                   # Salt Lake City
    us-west4                   # Las Vegas

    southamerica-east1         # São Paulo
    southamerica-west1         # Santiago

    europe-central2            # Warsaw
    europe-north1              # Finland
    europe-north2              # Stockholm
    europe-southwest1          # Madrid
    europe-west1               # Belgium
    europe-west2               # London
    europe-west3               # Frankfurt
    europe-west4               # Netherlands
    europe-west6               # Zurich
    europe-west8               # Milan
    europe-west9               # Paris
    europe-west10              # Berlin
    europe-west12              # Turin

    asia-east1                 # Taiwan
    asia-east2                 # Hong Kong
    asia-northeast1            # Tokyo
    asia-northeast2            # Osaka
    asia-northeast3            # Seoul
    asia-south1                # Mumbai
    asia-south2                # Delhi
    asia-southeast1            # Singapore
    asia-southeast2            # Jakarta

    australia-southeast1       # Sydney
    australia-southeast2       # Melbourne

    me-central1                # Doha
    me-central2                # Dammam
    me-west1                   # Tel Aviv
)

###############################################################################
# Domains
###############################################################################

declare -A DOMAINS

DOMAINS["global.anycastprivacy.org"]="${REGIONS[*]}"

DOMAINS["africa.anycastprivacy.org"]="
africa-south1
"

DOMAINS["asia.anycastprivacy.org"]="
asia-east1
asia-east2
asia-northeast1
asia-northeast2
asia-northeast3
asia-south1
asia-south2
asia-southeast1
asia-southeast2
"

DOMAINS["australia.anycastprivacy.org"]="
australia-southeast1
australia-southeast2
"

DOMAINS["europe.anycastprivacy.org"]="
europe-central2
europe-north1
europe-north2
europe-southwest1
europe-west1
europe-west2
europe-west3
europe-west4
europe-west6
europe-west8
europe-west9
europe-west10
europe-west12
"

DOMAINS["middleeast.anycastprivacy.org"]="
me-central1
me-central2
me-west1
"

DOMAINS["northamerica.anycastprivacy.org"]="
northamerica-northeast1
northamerica-northeast2
northamerica-south1
"

DOMAINS["us.anycastprivacy.org"]="
us-central1
us-east1
us-east4
us-east5
us-south1
us-west1
us-west2
us-west3
us-west4
"

DOMAINS["southamerica.anycastprivacy.org"]="
southamerica-east1
southamerica-west1
"
