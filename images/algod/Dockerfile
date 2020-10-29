FROM golang:1.13.12

ARG CHANNEL=nightly
ARG URL=
ARG BRANCH=
ARG SHA=
ARG BOOTSTRAP_URL=""

#ARG URL=https://github.com/algorand/go-algorand
#ARG BRANCH=master

ARG ALGOD_PORT="60000"
ARG KMD_PORT="60001"
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

# Configure network
RUN python3 /tmp/images/algod/setup.py configure \
 --bin-dir "$BIN_DIR" \
 --network-dir /opt/testnetwork \
 --network-template "${TEMPLATE}" \
 --network-token "${TOKEN}" \
 --algod-port "${ALGOD_PORT}" \
 --kmd-port "${KMD_PORT}" \
 --network "${NETWORK}" \
 --bootstrap-url "${ALGOD_BOOTSTRAP_URL}"

# Start algod
CMD ["/usr/bin/env", "bash", "-c", "/tmp/images/algod/setup.py start --bin-dir \"$BIN_DIR\" --network-dir \"/opt/testnetwork\""]
