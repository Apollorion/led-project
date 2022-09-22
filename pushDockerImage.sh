#!/bin/bash

set -e

# Check if GITHUB_TOKEN environment variable is set
if [ -z "$GITHUB_TOKEN" ]; then
  echo "GITHUB_TOKEN environment variable is not set"
  exit 1
fi

if [[ "$(uname -m)" != "aarch64" ]]; then
  echo "This script is only meant to be run on a Raspberry Pi 4"
  exit 1
fi


echo $GITHUB_TOKEN | docker login ghcr.io -u Apollorion --password-stdin

docker build -t ghcr.io/apollorion/led-project:aarch64 .
docker push ghcr.io/apollorion/led-project:aarch64
