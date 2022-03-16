#!/bin/bash

set -euo pipefail

# install poetry
sudo apt-get update
sudo apt-get install -y python3.9
sudo pip3 install poetry
