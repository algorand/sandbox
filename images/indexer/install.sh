#!/usr/bin/env bash

# Sometimes indexer is disabled, detect the missing build config.
if [ -z "${BRANCH}" ] || [ -z "${URL}"]; then
  echo "Missing BRANCH or URL environment variable. Skipping install."
  exit 0
fi

git clone --single-branch --branch "${BRANCH}" "${URL}" /opt/indexer
if [ "${SHA}" != "" ]; then
  echo "Checking out ${SHA}"
  git checkout "${SHA}";
fi
make
cp cmd/algorand-indexer/algorand-indexer /tmp
