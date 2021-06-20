FROM sandbox_algod:latest

ENV MNEMONICS_FILE="/tmp/mnemonics.txt"

WORKDIR /root/toketmaster
COPY ./toketmaster /root/toketmaster

RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN python3 -m pip install py-algorand-sdk pytest

COPY images/toketmaster/get_mnemonics.sh /tmp/get_mnemonics.sh
RUN /tmp/get_mnemonics.sh
