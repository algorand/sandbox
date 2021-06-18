#!/bin/bash

echo "Launch Script Called"

check_if_built_from_source () {
  if [ -d "/tmp/images/algod/go-algorand" ]; then
    return true
  else
    return false
  fi
}

if test `check_if_built_from_source` = true; then
  git pull && make && make install || /opt/start_algod.sh
else
  /bin/bash /tmp/images/algod/update.sh -d /opt/data -p /node
  /opt/start_algod.sh
fi

