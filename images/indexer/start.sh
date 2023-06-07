#!/bin/bash

# Start indexer daemon. There are various configurations controlled by
# environment variables.
#
# Configuration:
#   DISABLED          - If set start a server that returns an error instead of indexer.
#   CONNECTION_STRING - the postgres connection string to use.
#   PORT              - port to start indexer on.
set -e

THIS=$(basename "$0")

disabled() {
  echo "$THIS: running disabled.go script in lieu of indexer"
  go run /tmp/disabled.go -port "$PORT" -code 200 -message "Indexer disabled for this configuration."
}

echo "$THIS: starting indexer container script"

# Make sure data directory is available in case we're using a version that requires it.
export INDEXER_DATA=/tmp/indexer-data
mkdir -p ${INDEXER_DATA}

if [ -n "$DISABLED" ]; then
  disabled
elif [ ! -f /tmp/algorand-indexer ]; then
  echo "$THIS: binary not found at /tmp/algorand-indexer"
  exit 1
else
  /tmp/algorand-indexer daemon \
    --dev-mode \
    --server ":$PORT" \
    -P "$CONNECTION_STRING"
fi

sleep infinity
