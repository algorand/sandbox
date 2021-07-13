#!/usr/bin/env bash

# Build AlgoSearch and put binary in /tmp.
#
# Configured with environment variables:
#   URL    - Git repository URL.
#   BRANCH - Git branch to clone.
#   SHA    - (optional) Specific commit hash to checkout.
set -e

# Sometimes AlgoSearch is disabled, detect the missing build config.
if [ -z "${BRANCH}" ] || [ -z "${URL}" ]; then
  echo "Missing BRANCH or URL environment variable. Skipping install."
  exit 0
fi

git clone --single-branch --branch "${BRANCH}" "${URL}" /app
if [ "${SHA}" != "" ]; then
  echo "Checking out ${SHA}"
  git checkout "${SHA}";
fi
