#! /usr/bin/env bash

set -euo pipefail

if [[ -n "${PROJECT_DIR:-}" ]]; then
  cd ${PROJECT_DIR}
fi

export IMAGE_VERSION=${BRANCH_NAME_CLEAN}

poetry run pytest $1 --junitxml "${OUTPUT_DIR}/$1-report.xml" --html "${OUTPUT_DIR}/$1-report.html"
