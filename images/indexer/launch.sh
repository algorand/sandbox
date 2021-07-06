#!/bin/bash

echo "Launch script called"

git pull && make && make install || /tmp/start.sh

/tmp/start.sh

