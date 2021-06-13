#!/bin/bash

# Script automatically check and install any updates on the
# current release channel for the algod node
#
# No parameters

echo "Launch Script called"

if [ ! -z "$UPDATE_TRIGGER" ]; then
  UPDATE_TRIGGER=""
  /bin/bash /tmp/images/algod/update.sh -d /opt/data -p /node
fi

/bin/bash /opt/start_algod.sh
