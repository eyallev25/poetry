#! /usr/bin/env bash

set -euo pipefail

TEST_IMAGE_NAME=${TEST_IMAGE_NAME:-anun/tracer-benchmark}
TEST_IMAGE_TAG=${BRANCH_NAME_CLEAN:-latest}

SSH_DIR=${SSH_DIR:-~/.ssh/id_rsa}

DOCKER_BUILDKIT=1 docker build \
    --ssh bitbucket=${SSH_DIR} \
    -t ${TEST_IMAGE_NAME}:${TEST_IMAGE_TAG} \
    .