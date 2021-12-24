This is a fork and complete refactor of algorand/sandbox. The goal of this fork is to create a `docker-compose` stack that can be used for algorand development, including `pyteal`. The services can be run manually with `docker-compose` or you can use VSCode to run a devcontainer that comes pre-installed with the VSCode python extesnion.

# Using VSCode Remote Containers

## Requirements
* The system you are developing on must have `docker` and `docker-compose` installed.
* You must be able to use VSCode on the system running the docker daemon (either locally or via SSH)

## Adding .devcontainer Directory
It's recommended that you do your work in a git repository. It can be a new, empty, repository or one that already exists. Once in the directory, add this repo as a submodule in a directory name `.devcontainer`: `git submodule add https://github.com/joe-p/sandbox.git .devcontainer`

## Configuration
All configuration is done in the `.devcontainer/.env` file. It's recommended you start with `.devcontainer/example_envs/devcontainer.env`, which you can copy to `.devcontainer`: `cp .devcontainer/example_envs/devcontainer.env .devcontainer/.env`. 

Once you have copied that file, you need to set the user and group IDs for the container user with the `ALGO_UID` and `ALGO_GID` variables. These values should align with the ID's you use on the host. `id -u` and `id -g` will be helpful here.

## Reopen In Container

Once you have the `.env` configured, you can open your git repository in VSCode. Ensure `.devcontainer/` exists in the repo at the top level. Once the repository is open, open up the command pallet (`cmd+shift+p` or `ctrl+shift+p` and run `Remote-Containers: Reopen in Container`).

You should now be in the repository's directoy in the container, which is mounted to `/home/algo/workspace`

# Using docker-compose

## Requirements

The only hard requirement is that the system you are developing on must have `docker` and `docker-compose` installed. 

## Configuration

All of the configuration is done with the `.env` file at the root of this repository. The only necessary change you must make is changing the UID and GID to your own respective IDs. `id -u` and `id -g` will be helpful here. Once the IDs are set, you can continue without changing anything else. 

## Run Services

To start all of the services, use `docker-compose up`. This will run in the foreground showing build and runtime infomration. To run them in the background, use `docker-compose up -d`

## Attaching to Container

To attach to a container run `docker exec -it $CONTAINER_NAME /bin/bash`. The name of the container will depend on the name of directory this repository resides in, but an example of this command would be `docker exec -it sandbox_algod-pyteal_1 /bin/bash`

This will put you in the `/home/algo/workspace/` directory (on the container), which by default is a bind-mount of a host directory (by default it's `example_workspace/`)

## Running a test

Assuming you are still using the default configuration, once you are in `/home/algo/workspace` on the container you can run `./test.sh` which will generate a transaction and then start a debugging session for that transaction. The transaction creates a very simple application that simply returns 1 (see `example_workspace/test.teal`)

## Further Configuration

More example configurations can be found in `example_envs/`. To use an example configuration, just move the file to the root directory and change the name to `.env`