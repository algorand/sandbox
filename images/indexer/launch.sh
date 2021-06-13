#!/bin/bash

echo "Launch script called"

set -e

if [ ! -z "$UPDATE_TRIGGER" ]; then
  UPDATE_TRIGGER=""

  cd /opt/indexer
  git pull
  make
  cp cmd/algorand-indexer/algorand-indexer /tmp
else
  echo "No update triggered"
fi

/tmp/start.sh
