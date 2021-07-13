#!/usr/bin/env bash

# Start algosearch daemon. There are various configurations controlled by
# environment variables.
#
# Configuration:
#   DISABLED          - If set start a server that returns an error instead of algosearch.
set -e

start_service() {
  pm2-runtime process.yml
}

disabled() {
  node disabled.js
}

if [ ! -z "$DISABLED" ]; then
  disabled
else
  start_service
fi

sleep infinity
