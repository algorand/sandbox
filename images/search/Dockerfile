# pull official base image
FROM node:14.4.0-alpine

# Environment variables used by install.sh
ARG URL=https://github.com/kevguy/algosearch
ARG BRANCH=algod_v2
ARG SHA=""

# set working directory
ENV HOME /app
WORKDIR /app

ENV DEBIAN_FRONTEND noninteractive
RUN apk add --no-cache git bzip2 make bash

# add `/app/node_modules/.bin` to $PATH
ENV PATH /app/node_modules/.bin:$PATH

# Copy files to container.
COPY images/search/install.sh /tmp/install.sh

# Install indexer binaries.
RUN /tmp/install.sh

RUN cd /app

COPY images/search/global.js ./service/global.js

# install app dependencies
RUN npm install --silent && npm install pm2 -g

# add app
RUN npm run build --silent

# start app
EXPOSE 8000
CMD ["pm2-runtime", "process.yml"]
