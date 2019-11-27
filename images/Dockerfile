FROM ubuntu:18.04
ARG channel
ARG USER_ID
ARG GROUP_ID
ARG OSTYPE

RUN if [ ${OSTYPE} = Linux ] && [ ${USER_ID:-0} -ne 0 ] && [ ${GROUP_ID:-0} -ne 0 ]; then \
    groupadd -g ${GROUP_ID} algorand &&\
    useradd -l -u ${USER_ID} -g algorand algorand &&\
    chown --changes --silent --no-dereference --recursive \
          --from=33:33 ${USER_ID}:${GROUP_ID} \
        /opt \
;fi

ENV DEBIAN_FRONTEND noninteractive
RUN apt update && apt-get install -y ca-certificates
#ADD https://github.com/algorand/go-algorand-doc/raw/master/downloads/installers/linux_amd64/install_master_linux-amd64.tar.gz /tmp
ADD https://algorand-releases.s3.us-east-1.amazonaws.com/channel/stable/install_stable_linux-amd64_2.0.1.tar.gz /tmp

RUN \
  set -eux; \
  mkdir /opt/installer ; \
  cd /opt/installer ; \
  tar xvf /tmp/install*tar.gz ; \
  ./update.sh -i -c $channel -p /opt/algorand/node -d /opt/algorand/node/data.tmp -n ; \
  rm -rf /opt/algorand/node/data.tmp

ENTRYPOINT ["/opt/algorand/node/algod", "-d", "/opt/algorand/node/data"]
