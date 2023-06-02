#!/usr/bin/env bash

# Build conduit and put binary in /tmp.
#
# Configured with environment variables:
#   URL    - Git repository URL.
#   BRANCH - Git branch to clone.
#   SHA    - (optional) Specific commit hash to checkout.
set -e

START=$(date "+%s")
THIS=$(basename "$0")

echo "$THIS: starting conduit image install"

# Sometimes conduit is disabled, detect the missing build config.
if [ -z "${BRANCH}" ] || [ -z "${URL}" ]; then
  echo "Missing BRANCH or URL environment variable. Skipping install."
  # returning with 0 because it will run the disabled server.
  exit 0
fi

git clone --single-branch --branch "${BRANCH}" "${URL}" /opt/conduit
if [ "${SHA}" != "" ]; then
  echo "Checking out ${SHA}"
  git checkout "${SHA}";
fi
make
cp cmd/conduit/conduit /tmp

echo "$THIS: seconds it took to get to finish conduit image install: $(($(date "+%s") - START))s"
