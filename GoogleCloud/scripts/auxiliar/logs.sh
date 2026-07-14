#!/bin/bash

###############################################################################
# Logging
###############################################################################

write_log() {
    local level="$1"
    shift

    printf '[%s][%s] %s\n' "$level" "$(date +%Y%m%d_%H-%M-%S)" "$*"
}

log() {
    write_log INFO "$@"
}

warn() {
    write_log WARNING "$@"
}

error() {
    write_log ERROR "$@"
}

abort() {
    error "$@"
    exit 1
}
