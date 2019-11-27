# Algorand Sandbox

This is a fast way to create and configure an Algorand node and start developing.

You will need to install **Docker**, [instructions are available here](https://docs.docker.com/v17.09/engine/installation/).

# Usage

Use the **sandbox** command to interact with the Algorand Sandbox.
```
sandbox commands:
  up [mainnet||testnet||betanet] [-s||--use-snapshot]
          -> spin up the sandbox environment, uses testnet by default.
             Optionally provide -s to initialize data from a snapshot.
  down    -> tear down the sandbox environment
  restart -> restart the sandbox
  enter   -> enter the sandbox container
  clean   -> stops and deletes containers and data directory
  test    -> runs some tests to make sure everything is working correctly

algorand commands:
  logs        -> stream algorand logs with the carpenter utility
  status      -> get node status
  goal (args) -> run goal command like 'goal node status'

tutorials:
  introduction -> learn how to get Algos on testnet and create a transaction
```
