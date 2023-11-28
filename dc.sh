#!/bin/bash


docker run -d \
    -v /var/run/docker.sock:/var/run/docker.sock \
    -v "$PWD:$PWD" \
    -w="$PWD" \
    docker/compose:1.27.4 \
    -f ./docker-compose.yml up

