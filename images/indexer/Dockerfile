FROM golang:1.14.15

# Environment variables used by install.sh
ARG URL=https://github.com/algorand/indexer
ARG BRANCH=master
ARG SHA=""

ENV HOME /opt/indexer
WORKDIR /opt/indexer

# Basic dependencies.
ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y apt-utils curl git git-core bsdmainutils python3 libtool libboost-math-dev

# Copy files to container.
COPY images/indexer/disabled.go /tmp/disabled.go
COPY images/indexer/start.sh /tmp/start.sh
COPY images/indexer/install.sh /tmp/install.sh

# Install indexer binaries.
RUN /tmp/install.sh

CMD ["/tmp/start.sh"]
