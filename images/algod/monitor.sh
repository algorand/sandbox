#!/usr/bin/env bash

# Script to handle automatic updating before container startup
#
# No Parameters

# exit 1

set -e

if [ ! -z ALGOD_CHANNEL ] && [ ! -z INSTALL_SCRIPT_DIR ]; then
  [ "${INSTALL_SCRIPT_DIR}/install.sh -d ${BIN_DIR} -c ${ALGOD_CHANNEL}" ]
  echo $?
elif [ ! -z ALGOD_BRANCH ] && [ ! -z ALGOD_URL ] && [ ! -z INSTALL_SCRIPT_DIR ]; then
  [ "${INSTALL_SCRIPT_DIR}/install.sh -d ${BIN_DIR} -b ${ALGOD_BRANCH} -u ${ALGOD_URL} " ]
  echo $?
fi

/opt/start_algod.sh
