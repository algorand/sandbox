ARG GO_VERSION=1.23.3
FROM golang:$GO_VERSION

ARG CHANNEL=nightly
ARG URL=
ARG BRANCH=
ARG SHA=

# When these are set attempt to connect to a network.
ARG GENESIS_FILE=""
ARG BOOTSTRAP_URL=""

# Options for algod config
ARG ALGOD_PORT=""
ARG ALGOD_FOLLOWER_PORT=""
ARG KMD_PORT=""
ARG TOKEN=""
ARG TEMPLATE=""
ARG NETWORK_NUM_ROUNDS="30000"
ARG NODE_ARCHIVAL=""
ARG MAX_ACCOUNT_LOOKBACK=256

RUN echo "Installing from source. ${URL} -- ${BRANCH}"
ENV BIN_DIR="$HOME/node"
ENV ALGORAND_DATA="/opt/data"

# Basic dependencies.
ENV HOME /opt
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y apt-utils curl git git-core bsdmainutils python3

# Copy lots of things into the container. The gitignore indicates which directories.
COPY . /tmp

# Install algod binaries.
RUN /tmp/images/algod/install.sh \
    -d "${BIN_DIR}" \
    -c "${CHANNEL}" \
    -u "${URL}" \
    -b "${BRANCH}" \
    -s "${SHA}"

# Configure network
RUN sed -i \
  -e "s/NETWORK_NUM_ROUNDS/$NETWORK_NUM_ROUNDS/" \
  -e "s/ALGOD_FOLLOWER_PORT/$ALGOD_FOLLOWER_PORT/" \
  "//tmp/${TEMPLATE}" && \
 /tmp/images/algod/setup.py \
 --bin-dir "$BIN_DIR" \
 --data-dir "/opt/data" \
 --start-script "/opt/start_algod.sh" \
 --network-dir "/opt/testnetwork" \
 --network-template "//tmp/${TEMPLATE}" \
 --network-token "${TOKEN}" \
 --algod-port "${ALGOD_PORT}" \
 --kmd-port "${KMD_PORT}" \
 --bootstrap-url "${BOOTSTRAP_URL}" \
 --genesis-file "/tmp/${GENESIS_FILE}" \
 --archival "${NODE_ARCHIVAL}" \
 --max-account-lookback "${MAX_ACCOUNT_LOOKBACK}"

ENV PATH="$BIN_DIR:${PATH}"
WORKDIR /opt/data

# Start algod
CMD ["/opt/start_algod.sh"]
