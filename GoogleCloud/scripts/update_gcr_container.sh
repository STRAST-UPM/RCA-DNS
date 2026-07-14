#!/bin/bash
set -euo pipefail

readonly SERVICE_REPO_URL="https://github.com/STRAST-UPM/base_service_js"
readonly SERVICE_IMAGE_NAME="base_service_js"
readonly SERVICE_LOCAL_IMAGE="strast-upm/base_service_js"
readonly SERVICE_IMAGE_TAG="rcadns"
readonly GCR_REGISTRY="gcr.io"

resolve_project_id() {
    if [[ -n "${PROJECT_ID:-}" ]]; then
        printf '%s\n' "$PROJECT_ID"
        return
    fi

    gcloud config get-value project 2>/dev/null
}

update_gcr_container() {
    local project_id
    local temp_dir
    local checkout_dir
    local gcr_tag

    project_id="$(resolve_project_id)"
    if [[ -z "$project_id" ]]; then
        echo "No Google Cloud project is configured. Run: gcloud config set project <PROJECT_ID>" >&2
        exit 1
    fi

    echo "Project ID: $project_id"

    temp_dir="$(mktemp -d)"
    checkout_dir="$temp_dir/base_service_js"

    cleanup() {
        rm -rf "$temp_dir"
    }

    trap cleanup RETURN
    # Clone repo
    echo "Cloning ${SERVICE_REPO_URL}..."
    git clone --depth 1 "$SERVICE_REPO_URL" "$checkout_dir"
    # Build image
    echo "Building image ${SERVICE_IMAGE_NAME}:${SERVICE_IMAGE_TAG}..."
    docker build --no-cache --force-rm -t "$SERVICE_LOCAL_IMAGE:$SERVICE_IMAGE_TAG" "$checkout_dir"
    # Push image to GCR
    echo "Authenticating Docker with ${GCR_REGISTRY}..."
    gcloud auth configure-docker "$GCR_REGISTRY" --quiet

    gcr_tag="$GCR_REGISTRY/$project_id/$SERVICE_IMAGE_NAME:$SERVICE_IMAGE_TAG"
    echo "Pushing ${gcr_tag}..."
    docker tag "$SERVICE_LOCAL_IMAGE:$SERVICE_IMAGE_TAG" "$gcr_tag"
    docker push "$gcr_tag"

    echo "Cleaning intermediate images..."
    docker image prune -f

    echo "Completed: $gcr_tag"
}

if [[ "${BASH_SOURCE[0]}" == "$0" ]]; then
    update_gcr_container "$@"
fi