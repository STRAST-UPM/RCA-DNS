#!/bin/bash

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