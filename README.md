# Algorand Sandbox

This is a fast way to create and configure an Algorand development environment with [Algod](https://github.com/algorand/go-algorand) and [Indexer](https://github.com/algorand/indexer).

You will need to install **Docker Compose**, [instructions are available here](https://docs.docker.com/compose/install/).

**Warning**: Algorand Sandbox is *not* meant for production environments and should *not* be used to store secure Algorand keys. Updates may reset all the data and keys that are stored.

## Usage

Use the **sandbox** command to interact with the Algorand Sandbox.
```
sandbox commands:
  up    [config]  -> start the sandbox environment.
  down            -> tear down the sandbox environment.
  reset           -> reset the containers to their initial state.
  clean           -> stops and deletes containers and data directory.
  test            -> runs some tests to demonstrate usage.
  enter [algod||indexer||indexer-db]
                  -> enter the sandbox container.
  version         -> print binary versions.
  copyTo <file>   -> copy <file> into the algod container. Useful for offline transactions & LogicSigs plus TEAL work.
  copyFrom <file> -> copy <file> from the algod container. Useful for offline transactions & LogicSigs plus TEAL work.

algorand commands:
  logs            -> stream algorand logs with the carpenter utility.
  status          -> get node status.
  goal (args)     -> run goal command like 'goal node status'.
  tealdbg (args)  -> run tealdbg command to debug program execution.

special flags for 'up' command:
  -v|--verbose           -> display verbose output when starting standbox.
  -s|--skip-fast-catchup -> skip catchup when connecting to real network.
  -i|--interactive       -> start docker-compose in interactive mode.
```

Sandbox creates the following API endpoints:
* `algod`:
  * address: `http://localhost:4001`
  * token: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`
* `kmd`:
  * address: `http://localhost:4002`
  * token: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`
* `indexer`:
  * address: `http://localhost:8980`

## Getting Started

### Ubuntu and macOS

Make sure the docker daemon is running and docker-compose is installed.

Open a terminal and run:
```
git clone https://github.com/algorand/sandbox.git
cd sandbox
./sandbox up
```

Note for Ubuntu: You may need to alias `docker` to `sudo docker` or follow the steps in https://docs.docker.com/install/linux/linux-postinstall so that a non-root user can user the command `docker`.

Run the test command for examples of how to interact with the environment:
```
./sandbox test
```

### Windows

1. Install Git for Windows: https://gitforwindows.org/
2. Install and launch Docker for Windows: https://docs.docker.com/get-docker
3. Open "Git Bash" and follow the instruction for Ubuntu and macOS above, in the "Git Bash" terminal.

## Private Network vs Real Network

Sandbox supports two primary modes of operation. By default, a private network will be created, which is only available from the local environment. There is also a real network mode which will connect you to one of the long running Algorand networks and allow you to interact with it.

### Private Network

By default you will be given access to a private network. This environment is preloaded with a number of accounts ready to use for testing transactions, and includes an `Indexer` service configured to synchronize against the private network. Because it doesn't require catching up to one of the long running networks it also starts very quickly.

There is also a `dev` configuration that runs a private network with a dev mode network. In this configuration, every transaction being sent to the node automatically will generate a new block, rather than wait for a new round in real time. 

### Real Network

The `mainnet`, `testnet`, `betanet`, and `devnet` configurations configure the sandbox to connect to one of those long running networks. Once started it will automatically attempt to catchup to the latest round. Catchup tends to take a while and a progress bar will be displayed to keep you informed of the progress.

Due to technical limitations, this configuration does not contain preconfigured accounts that you can immediately transact with, and Indexer is not available.

## Working with files

Some Algorand commands require using a file for the input. For example working with TEAL programs. In some other cases like working with Logical signatures or transactions offline you may need to get a file output from LogicSig or transaction.

To stage a file use the `copyTo` command. The file will be placed in the algod data directory, which is where sandbox executes `goal`. This means the files can be used without specifying their full path.

To copy a file from sandbox (algod instance) use the `copyFrom` command. The file will be copied to sandbox directory on host filesystem.

#### copyTo example: 

these commands will stage two TEAL programs then use them in a `goal` command:
```
~$ ./sandbox copyTo approval.teal
~$ ./sandbox copyTo clear.teal
~$ ./sandbox goal app create --approval-prog approval.teal --clear-prog clear.teal --creator YOUR_ACCOUNT  --global-byteslices 1 --global-ints 1 --local-byteslices 1 --local-ints 1
```

#### copyFrom example: 

these commands will create and copy a signed logic transaction file, created by `goal`, to be sent or communicated off the chain (e.g. by email or as a QR Code) and submitted else where:
```
~$ ./sandbox goal clerk send -f <source-account> -t <destination-account> --fee 1000 -a 1000000 -o "unsigned.txn"
~$ ./sandbox goal clerk sign --infile unsigned.txn --outfile signed.txn
~$ ./sandbox copyFrom "signed.txn"
```

## Advanced configurations

The sandbox environment is completely configured using the `config.*` files in the root of this repository. For example, the default configuration is **config.nightly**:
```
export ALGOD_CHANNEL="nightly"
export ALGOD_URL=""
export ALGOD_BRANCH=""
export ALGOD_SHA=""
export ALGOD_BOOTSTRAP_URL=""
export ALGOD_GENESIS_FILE=""
export INDEXER_URL="https://github.com/algorand/indexer"
export INDEXER_BRANCH="develop"
export INDEXER_SHA=""
export INDEXER_DISABLED=""
```

Indexer is always built from source since it can be done quickly. For most configurations, algod will be installed using our standard release channels, but building from source is also available by setting the git URL, Branch and optionally a specific SHA commit hash.

The **up** command looks for the config extension based on the argument provided. If you have a custom configuration pointed to a fork, you can start the sandbox with your code:
```
export ALGOD_CHANNEL=""
export ALGOD_URL="https://github.com/<user>/go-algorand"
export ALGOD_BRANCH="my-test-branch"
export ALGOD_SHA=""
export ALGOD_BOOTSTRAP_URL=""
export ALGOD_GENESIS_FILE=""
export INDEXER_URL="https://github.com/<user>/go-algorand"
export INDEXER_BRANCH="develop"
export INDEXER_SHA=""
export INDEXER_DISABLED=""
```

## Debugging for teal developers

For detailed information on how to debug smart contracts and use tealdbg CLI,please consult with [Algorand Development Portal :: Smart Contract Debugging](https://developer.algorand.org/docs/features/asc1/debugging/#setting-the-debugger-context).

Algorand smart contract debugging process uses `tealdbg` command line of algod instance(algod container in sandbox).

**Note**: Always use `tealdbg` with `--listen 0.0.0.0` or `--listen [IP ADDRESS]` flags, if you need to access tealdbg from outside of algod docker container!

#### tealdbg examples:

Debugging smart contract with Chrome Developer Tools (CDT):
```~$ ./sandbox tealdbg debug ${TEAL_PROGRAM} -f cdt -d dryrun.json```

Debugging smart contract with Web Interface (primal web UI)
```~$ ./sandbox tealdbg debug ${TEAL_PROGRAM} -f web -d dryrun.json```
  
The debugging endpoint port (default 9392) is forwarded directly to the host machine and can be used directly by Chrome Dev Tools for debugging Algorand TEAL smart comtracts (Goto url chrome://inspect/ and configure port 9392 before using please).

Note: If you change the port by running `tealdbg --port YOUR_PORT` then please modify the docker-compose.yml file and change all occurances of mapped 9392 port with your desired one.

## Errors

If something goes wrong, check the `sandbox.log` file for details.
