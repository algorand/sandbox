FROM golang:1.13.12-alpine

ARG URL=https://github.com/algorand/indexer
ARG BRANCH=master
ARG SHA=""
ARG DISABLED=""

RUN echo "Installing from source. ${URL} -- ${BRANCH} -- ${SHA}"

ENV DEBIAN_FRONTEND noninteractive
RUN apk add --no-cache git bzip2 make bash

# Install indexer binaries.
COPY images/indexer/install.sh /tmp/install.sh
ENV HOME /opt/indexer
WORKDIR /opt/indexer
RUN /tmp/install.sh

COPY images/indexer/disabled.go /tmp/disabled.go
COPY images/indexer/start.sh /tmp/start.sh
COPY images/indexer/data/* /tmp/

RUN ls -lh /tmp

CMD ["/tmp/start.sh"]
