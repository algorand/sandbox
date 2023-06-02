#!/usr/bin/env bash

# Build indexer and put binary in /tmp.
#
# Configured with environment variables:
#   URL    - Git repository URL.
#   BRANCH - Git branch to clone.
#   SHA    - (optional) Specific commit hash to checkout.
set -e

START=$(date "+%s")
THIS=$(basename "$0")

echo "$THIS: starting indexer image install"

# Sometimes indexer is disabled, detect the missing build config.
if [ -z "${BRANCH}" ] || [ -z "${URL}" ]; then
  echo "Missing BRANCH or URL environment variable. Skipping install."
  # returning with 0 because it will run the disabled server.
  exit 0
fi

git clone --single-branch --branch "${BRANCH}" "${URL}" /opt/indexer
if [ "${SHA}" != "" ]; then
  echo "Checking out ${SHA}"
  git checkout "${SHA}";
fi
make
cp cmd/algorand-indexer/algorand-indexer /tmp

echo "$THIS: seconds it took to get to finish indexer image install: $(($(date "+%s") - START))s"
