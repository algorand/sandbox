#!/bin/bash

# Start indexer daemon. There are various configurations controlled by
# environment variables.
#
# Configuration:
#   DISABLED          - If set start a server that returns an error instead of indexer.
#   CONNECTION_STRING - the postgres connection string to use.
#   SNAPSHOT          - snapshot to import, if set don't connect to algod.
#   PORT              - port to start indexer on.
#   ALGOD_ADDR        - host:port to connect to for algod.
#   ALGOD_TOKEN       - token to use when connecting to algod.
set -e

THIS=$(basename "$0")

start_with_algod() {
  echo "$THIS: starting indexer against algod (empty SNAPSHOT=$SNAPSHOT)"

  # wait for algod to start
  for i in 1 2 3 4 5; do
    wget "${ALGOD_ADDR}"/genesis -O genesis.json && break
    echo "$THIS: ($i) Algod not responding... waiting."
    sleep 15
  done

  if [ ! -f genesis.json ]; then
    echo "$THIS: Failed to create genesis file!"
    exit 1
  fi

  echo "$THIS: Algod detected, genesis.json downloaded."
  echo "$THIS: Starting algorand-indexer."
  /tmp/algorand-indexer daemon \
    --dev-mode \
    --server ":$PORT" \
    -P "$CONNECTION_STRING" \
    --algod-net "${ALGOD_ADDR}" \
    --algod-token "${ALGOD_TOKEN}" \
    --genesis "genesis.json"
}

import_and_start_readonly() {
  echo "$THIS: Starting indexer with DB."

  # Extract the correct dataset
  ls -lh  /tmp
  mkdir -p /tmp/indexer-snapshot
  echo "$THIS: Extracting ${SNAPSHOT}"
  tar -xf "${SNAPSHOT}" -C /tmp/indexer-snapshot

  /tmp/algorand-indexer import \
    -P "$CONNECTION_STRING" \
    --genesis "/tmp/indexer-snapshot/algod/genesis.json" \
    /tmp/indexer-snapshot/blocktars/*

  /tmp/algorand-indexer daemon \
    --dev-mode \
    --server ":$PORT" \
    -P "$CONNECTION_STRING"
}

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
elif [ -z "${SNAPSHOT}" ]; then
  start_with_algod
else
  import_and_start_readonly
fi

sleep infinity
