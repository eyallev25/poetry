#! /usr/bin/env bash

set -euo pipefail

TEST_IMAGE_NAME=${TEST_IMAGE_NAME:-anun/tracer-benchmark}
TEST_IMAGE_TAG=${BRANCH_NAME_CLEAN:-latest}

DOCKER_BUILDKIT=1 docker build \
    -t ${TEST_IMAGE_NAME}:${TEST_IMAGE_TAG} \
    .