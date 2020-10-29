FROM golang:1.13.12-alpine

ARG URL=https://github.com/algorand/indexer
ARG BRANCH=master
ARG SHA=""

RUN echo "Installing from source. ${URL} -- ${BRANCH} -- ${SHA}"

ENV DEBIAN_FRONTEND noninteractive
RUN apk add --no-cache git bzip2 make bash

# Install indexer binaries.
RUN git clone --single-branch --branch "${BRANCH}" "${URL}" /opt/indexer
ENV HOME /opt/indexer
WORKDIR /opt/indexer
RUN if [ "${SHA}" != "" ]; then echo "Checking out ${SHA}" && git checkout "${SHA}"; fi
RUN make
RUN cp cmd/algorand-indexer/algorand-indexer /tmp

COPY images/indexer/disabled.go /tmp/disabled.go
COPY images/indexer/setup.sh /tmp/setup.sh
COPY images/indexer/data/* /tmp/

RUN ls -lh /tmp

CMD ["/tmp/setup.sh"]
