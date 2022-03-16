#! /usr/bin/env bash

set -euo pipefail

IMAGE_NAME=${IMAGE_NAME:-anun/tracer_image}
IMAGE_TAG=${IMAGE_TAG:-0.0.1}

SSH_DIR=${SSH_DIR:-~/.ssh/id_rsa}

DOCKER_BUILDKIT=1 docker build \
    --ssh bitbucket=${SSH_DIR} \
    -t ${IMAGE_NAME}:${IMAGE_TAG} \
    .