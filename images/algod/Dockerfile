FROM golang:1.13.12

ARG CHANNEL=nightly
ARG URL=
ARG BRANCH=
ARG SHA=

# When these are set attempt to connect to a network.
ARG GENESIS_FILE=""
ARG BOOTSTRAP_URL=""

#ARG URL=https://github.com/algorand/go-algorand
#ARG BRANCH=master

ARG ALGOD_PORT="4001"
ARG KMD_PORT="4002"
ARG TOKEN="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
ARG TEMPLATE="/tmp/images/algod/future_template.json"

RUN echo "Installing from source. ${URL} -- ${BRANCH}"
ENV BIN_DIR="$HOME/node"

ENV DEBIAN_FRONTEND noninteractive

# Basic dependencies.
ENV HOME /opt
RUN apt-get update && apt-get install -y apt-utils curl git git-core bsdmainutils python3

# Copy everything into the container.
COPY . /tmp

RUN rm -rf "${BIN_DIR}" && mkdir -p "${BIN_DIR}"

# Install algod binaries.
RUN /tmp/images/algod/install.sh \
    -d "${BIN_DIR}" \
    -c "${CHANNEL}" \
    -u "${URL}" \
    -b "${BRANCH}" \
    -s "${SHA}"

RUN find "${BIN_DIR}"

RUN find /tmp

# Configure network
RUN python3 /tmp/images/algod/setup.py configure \
 --bin-dir "$BIN_DIR" \
 --network-dir /opt/testnetwork \
 --network-template "${TEMPLATE}" \
 --network-token "${TOKEN}" \
 --algod-port "${ALGOD_PORT}" \
 --kmd-port "${KMD_PORT}" \
 --bootstrap-url "${BOOTSTRAP_URL}" \
 --genesis-file "/tmp/${GENESIS_FILE}"

RUN find /tmp
# Start algod
CMD ["/usr/bin/env", "bash", "-c", "/tmp/images/algod/setup.py start --bin-dir \"$BIN_DIR\" --network-dir \"/opt/testnetwork\""]
