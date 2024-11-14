ARG GO_VERSION=1.23.3
FROM golang:$GO_VERSION-alpine

# Environment variables used by install.sh
ARG URL=https://github.com/algorand/conduit
ARG BRANCH=master
ARG SHA=""

ENV HOME /opt/conduit
WORKDIR /opt/conduit

ENV DEBIAN_FRONTEND noninteractive
RUN apk add --no-cache git make bash

# Copy files to container.
COPY images/conduit/disabled.go /tmp/disabled.go
COPY images/conduit/start.sh /tmp/start.sh
COPY images/conduit/install.sh /tmp/install.sh

# Install conduit binaries.
RUN /tmp/install.sh

CMD ["/tmp/start.sh"]
