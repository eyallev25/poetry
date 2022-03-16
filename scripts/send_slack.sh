#! /usr/bin/env bash

set -euo pipefail

if [[ -n "${PROJECT_DIR:-}" ]]; then
  cd ${PROJECT_DIR}
fi


# poetry run python send_slack.py || true
echo "Send tests status to slack channel"