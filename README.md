This is a fork and complete refactor of algorand/sandbox.

# Requirements

The only hard requirement is that the system you are developing on must have `docker` and `docker-compose` installed. 

# Getting Started

## Configuration

All of the configuration is done with the `.env` file at the root of this repository. The only necessary change you must make is changing the UID and GID to your own respective IDs. `id -u` and `id -g` will be helpful here. Once the IDs are set, you can continue without changing anything else. 

## Build Images

Clone this repo and run the following command to build the necessary images and start the services we need:

`docker-compose up --build`

## Run Services
You notice the above command will take over your terminal. You can press `Ctrl+C` to stop the services, then to run them as a daemon, run the following command:

`docker-compose up -d`

## Attaching to Container

To attach to the container run the following command:

`docker exec -it sandbox_algod-pyteal_1 /bin/bash`

This will put you in the `~/workspace/` directory, which by default is a bind-mount of `example_workspace/`

## Running a test

Assuming you are still using the default configuration, once you are in `~/workspace` on the container you can run `./test.sh` which will generate a transaction and then start a debugging session for that transaction. The transaction creates a very simple application that simply returns 1 (see `example_workspace/test.teal`)

## Further Configuration

More example configurations can be found in `example_envs/`. To use an example configuration, just move the file to the root directory and change the name to `.env`