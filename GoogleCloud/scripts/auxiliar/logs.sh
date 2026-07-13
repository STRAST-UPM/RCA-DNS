#!/bin/bash

###############################################################################
# Logging
###############################################################################

write_log() {
    local level="$1"
    shift

    printf '[%s] %s\n' "$level" "$*" | tee -a "$LOG_FILE"
}

log() {
    write_log INFO "$@"
}

warn() {
    printf '[WARNING] %s\n' "$*" | tee -a "$LOG_FILE" >&2
}

error() {
    printf '[ERROR] %s\n' "$*" | tee -a "$LOG_FILE" >&2
}

abort() {
    error "$@"
    exit 1
}