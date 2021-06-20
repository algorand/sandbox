FROM sandbox_algod:latest

ARG MNEMONICS_FILE=/tmp/config/mnemonics_privnet.txt

WORKDIR /root/toketmaster
COPY ./toketmaster /root/toketmaster
COPY ./config/mnemonics_testnet.txt /tmp/config/mnemonics_testnet.txt

RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN python3 -m pip install py-algorand-sdk pytest

COPY images/toketmaster/get_privnet_mnemonics.sh /tmp/get_privnet_mnemonics.sh
RUN /tmp/get_privnet_mnemonics.sh
