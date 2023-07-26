#!/bin/bash

# Start conduit daemon. There are various configurations controlled by
# environment variables.
#
# Configuration:
#   DISABLED          - If set start a server that returns an error instead of conduit.
#   CONNECTION_STRING - the postgres connection string to use.
#   ALGOD_ADDR        - host:port to connect to for algod follower.
#   ALGOD_ADMIN_TOKEN - the algod admin token.
#   PORT              - port to start conduit on.
set -e

THIS=$(basename "$0")

disabled() {
  echo "$THIS: running disabled.go script in lieu of conduit"
  go run /tmp/disabled.go -port "$PORT" -code 200 -message "Conduit disabled for this configuration."
}

echo "$THIS: starting conduit container script"

# Make sure data directory is available in case we're using a version that requires it.
export CONDUIT_DATA=/tmp/conduit-data
mkdir -p ${CONDUIT_DATA}

if [ -n "$DISABLED" ]; then
  disabled
elif [ ! -f /tmp/conduit ]; then
  echo "$THIS: binary not found at /tmp/conduit"
  exit 1
else
  /tmp/conduit init --importer algod --exporter postgresql > "${CONDUIT_DATA}"/conduit.yaml
  sed -i \
    -e "s/netaddr: \".*\"/netaddr: \"$ALGOD_ADDR\"/" \
    -e "s/token: \".*\"/token: \"$ALGOD_ADMIN_TOKEN\"/" \
    -e "s/addr: \":9999\"/addr: \":$PORT\"/" \
    -e "s/mode: OFF/mode: ON/" \
    -e "s/host= port=5432 user= password= dbname=/$CONNECTION_STRING/" \
    -e "s/retry-delay: \"1s\"/retry-delay: \"0s\"/" \
    "${CONDUIT_DATA}"/conduit.yaml

  cat "${CONDUIT_DATA}"/conduit.yaml

  /tmp/conduit -d "${CONDUIT_DATA}"
fi
