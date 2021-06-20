FROM sandbox_algod:latest

WORKDIR /root/toketmaster
COPY ./toketmaster /root/toketmaster

RUN apt update
RUN apt install python3 -y
RUN apt install python3-pip -y
RUN python3 -m pip install py-algorand-sdk pytest
