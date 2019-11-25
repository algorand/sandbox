# Algorand Sandbox

This is a fast way to create and configure an Algorand node and start developing.

You will need to install **Docker**, [instructions are available here](https://docs.docker.com/v17.09/engine/installation/).

# Usage

Use the **sandbox** command to interact with the Algorand Sandbox.
```
sandbox commands:
  up (mainnet||testnet||betanet) -> spin up the sandbox environment
  down                           -> tear down the sandbox environment
  restart                        -> restart the sandbox
  enter                          -> enter the sandbox container
  logs                           -> stream algorand logs with the carpenter utility
  status                         -> get node status
  goal (args)                    -> run goal command like 'goal node status'
  clean                          -> stops and deletes containers and data directory
```
