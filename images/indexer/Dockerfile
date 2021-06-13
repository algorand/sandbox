FROM golang:1.13.12-alpine

# Environment variables used by install.sh
ARG URL=https://github.com/algorand/indexer
ARG BRANCH=master
ARG SHA=""

# Trigger variables for launch script
ENV UPDATE_TRIGGER="${UPDATE_TRIGGER}"

ENV HOME /opt/indexer
WORKDIR /opt/indexer

ENV DEBIAN_FRONTEND noninteractive
RUN apk add --no-cache git bzip2 make bash

# Copy files to container.
COPY images/indexer/disabled.go /tmp/disabled.go
COPY images/indexer/start.sh /tmp/start.sh
COPY images/indexer/install.sh /tmp/install.sh
COPY images/indexer/launch.sh /tmp/launch.sh

# Install indexer binaries.
RUN /tmp/install.sh

CMD ["/tmp/launch.sh"]
