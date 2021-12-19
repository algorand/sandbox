ARG GO_VERSION=1.17.5
FROM golang:$GO_VERSION

ARG CHANNEL=stable
ARG URL=
ARG BRANCH=
ARG SHA=

# When these are set attempt to connect to a network.
ARG GENESIS_FILE=""
ARG BOOTSTRAP_URL=""

# Options for algod config
ARG ALGOD_PORT="4001"
ARG KMD_PORT="4002"
ARG TOKEN="aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
ARG TEMPLATE="images/algod/template.json"

ENV ALGORAND_DATA="/opt/data"

ARG ALGO_UID=""
ARG ALGO_GID=""

RUN apt-get update && apt-get install -y apt-utils curl git git-core bsdmainutils python3 python3-pip
#RUN pip3 install pyteal

# Copy lots of things into the container. The gitignore indicates which directories.
COPY . /tmp

ENV BIN_DIR="/opt/node"

# Install algod binaries.
RUN /tmp/images/algod/install.sh \
    -d "${BIN_DIR}" \
    -c "${CHANNEL}" \
    -u "${URL}" \
    -b "${BRANCH}" \
    -s "${SHA}"

# Configure network
RUN /tmp/images/algod/setup.py \
 --bin-dir "${BIN_DIR}" \
 --data-dir "${ALGORAND_DATA}" \
 --start-script "/opt/start_algod.sh" \
 --network-dir "/opt/testnetwork" \
 --network-template "/tmp/${TEMPLATE}" \
 --network-token "${TOKEN}" \
 --algod-port "${ALGOD_PORT}" \
 --kmd-port "${KMD_PORT}" \
 --bootstrap-url "${BOOTSTRAP_URL}" \
 --genesis-file "/tmp/${GENESIS_FILE}"

ENV PATH="$BIN_DIR:${PATH}"

RUN chown -R ${ALGO_UID}:${ALGO_GID} /opt/
RUN groupadd -g ${ALGO_GID} algo
RUN useradd -u ${ALGO_UID} -g ${ALGO_GID} -m algo

# Start algod
CMD ["/opt/start_algod.sh"]
