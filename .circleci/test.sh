#!/usr/bin/env bash
set -euxo pipefail

trap 'catch $?' ERR

catch() {
  echo "============= algod ============="
  ./sandbox dump algod
  echo "============= conduit ============="
  ./sandbox dump conduit
  echo "============= indexer ============="
  ./sandbox dump indexer
  exit $1
}

./sandbox up -v $CONFIG
