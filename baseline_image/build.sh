#! /usr/bin/env bash

set -euo pipefail

IMAGE_NAME=${IMAGE_NAME:-anun/baseline_image}
IMAGE_TAG=${IMAGE_TAG:-0.0.1}


DOCKER_BUILDKIT=1 docker build \
    -t ${IMAGE_NAME}:${IMAGE_TAG} \
    .