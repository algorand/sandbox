# Algorand Sandbox

This is a fast way to create and configure an Algorand node and start developing.

You will need to install **Docker**, [instructions are available here](https://docs.docker.com/get-docker/).

**Warning**: Algorand Sandbox is *not* meant for production environments and should *not* be used to store secure Algorand keys. Updates may reset all the data and keys that are stored.

## Usage

Use the **sandbox** command to interact with the Algorand Sandbox.
```
sandbox commands:
  up [mainnet||testnet||betanet] [-s||--skip-snapshot]
          -> spin up the sandbox environment, uses testnet by default.
             Optionally provide -s to skip initializing with a snapshot.
  down    -> tear down the sandbox environment
  restart -> restart the sandbox
  enter   -> enter the sandbox container
  clean   -> stops and deletes containers and data directory
  test    -> runs some tests to make sure everything is working correctly

algorand commands:
  logs        -> stream algorand logs with the carpenter utility
  status      -> get node status
  goal (args) -> run goal command like 'goal node status'
  dryrun (tx) -> run 'goal clerk dryrun -t tx' to test a transaction


tutorials:
  introduction -> learn how to get Algos on testnet and create a transaction
```

Sandbox creates the following API endpoints:
* `algod`: 
  * address: `http://localhost:4001`
  * token: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`
* `kmd`:
  * address: `http://localhost:4002`
  * token: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`

## Getting Started

### Ubuntu and macOS

Install and launch Docker (https://docs.docker.com/get-docker). 
Open a terminal and run:
```
git clone https://github.com/algorand/sandbox.git
cd sandbox
./sandbox up
```

Note for Ubuntu: You may need to alias `docker` to `sudo docker` or follow the steps in https://docs.docker.com/install/linux/linux-postinstall so that a non-root user can user the command `docker`.

You can then do the tutorial:
```
./sandbox introduction
```

### Windows

1. Install Git for Windows: https://gitforwindows.org/
2. Install and launch Docker for Windows: https://docs.docker.com/get-docker
3. Open "Git Bash" and follow the instruction for Ubuntu and macOS above, in the "Git Bash" terminal.
