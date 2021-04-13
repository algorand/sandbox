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

<<<<<<< HEAD
=======
#git clone --single-branch --branch "${BRANCH}" "${URL}" /opt/algosearch
>>>>>>> d47cfcf (feat: added algosearch support)
git clone --single-branch --branch "${BRANCH}" "${URL}" /app
if [ "${SHA}" != "" ]; then
  echo "Checking out ${SHA}"
  git checkout "${SHA}";
fi
<<<<<<< HEAD
=======
echo << "fuck"
#ls -l /opt/algosearch
#cp /opt/algosearch /app
>>>>>>> d47cfcf (feat: added algosearch support)
