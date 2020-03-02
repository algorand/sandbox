FROM ubuntu:18.04
ARG channel

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && apt-get install -y ca-certificates

# Use a non-privilidged user with a random UID / GID for security reasons
RUN groupadd -g 10353 algorand && \
  useradd -m -u 10353 -g algorand algorand && \
  chown -R algorand:algorand /opt && \
  ls -lha /opt

USER algorand

#ADD https://github.com/algorand/go-algorand-doc/raw/master/downloads/installers/linux_amd64/install_master_linux-amd64.tar.gz /tmp
ADD --chown=algorand:algorand https://algorand-releases.s3.us-east-1.amazonaws.com/channel/stable/install_stable_linux-amd64_2.0.4.tar.gz /tmp

RUN \
  set -eux; \
  mkdir /opt/installer ; \
  cd /opt/installer ; \
  tar xvf /tmp/install*tar.gz ; \
  ./update.sh -i -c $channel -p /opt/algorand/node -d /opt/algorand/node/data.tmp -n ; \
  rm -rf /opt/algorand/node/data.tmp ; \
  mkdir /opt/algorand/node/data

COPY ./config/start.sh /opt/algorand

VOLUME /opt/algorand/node/data

# Set up environment variable to make life easier
ENV PATH="/opt/algorand/node:${PATH}"
ENV ALGORAND_DATA="/opt/algorand/node/data"

ENTRYPOINT [ "/opt/algorand/start.sh" ]
