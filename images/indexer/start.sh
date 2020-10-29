#!/bin/bash

# Start indexer daemon. There are various configurations controlled by
# environment variables.
#
# Configuration:
#   DISABLED          - If set start a server that returns an error instead of indexer.
#   CONNECTION_STRING - the postgres connection string to use.
#   SNAPSHOT          - snapshot to import, if set don't connect to algod.
#   PORT              - port to start indexer on.
set -e

start_with_algod() {
  echo "Starting indexer against algod."

  for i in 1 2 3 4 5; do
    wget algod:4001/genesis -O genesis.json && break
    echo "Algod not responding... waiting."
    sleep 15
  done

  /tmp/algorand-indexer daemon \
    --server ":$PORT" \
    -P "$CONNECTION_STRING" \
    --algod-net "algod:4001" \
    --algod-token aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa \
    --genesis "genesis.json"
}

import_and_start_readonly() {
  echo "Starting indexer with DB."

  # Extract the correct dataset
  ls -lh  /tmp
  mkdir -p /tmp/indexer-snapshot
  echo "Extracting ${SNAPSHOT}"
  tar -xf "${SNAPSHOT}" -C /tmp/indexer-snapshot

  /tmp/algorand-indexer import \
    -P "$CONNECTION_STRING" \
    --genesis "/tmp/algod/genesis.json" \
    /tmp/indexer-snapshot/blocktars/*

  /tmp/algorand-indexer daemon \
    --server ":$PORT" \
    -P "$CONNECTION_STRING"
}

disabled() {
  go run /tmp/disabled.go -port "$PORT" -code 400 -message "Indexer disabled for this configuration."
}

if [ ! -z "$DISABLED" ]; then
  disabled
elif [ -z "${SNAPSHOT}" ]; then
  start_with_algod
else
  import_and_start_readonly
fi

sleep infinity
