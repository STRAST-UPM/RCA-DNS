#!/bin/bash

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
