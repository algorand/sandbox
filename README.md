# Algorand Sandbox

This is a fast way to create and configure an Algorand development environment with [Algod](https://github.com/algorand/go-algorand) and [Indexer](https://github.com/algorand/indexer).

**Docker Compose**  _MUST_ be installed. [Instructions](https://docs.docker.com/compose/install/).

On a *Windows* machine, **Docker Desktop** comes with the necessary tools. Please see the [Windows](#windows) section in getting started for more details.

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
```
In whatever local directory the sandbox should reside. Then:
```
cd sandbox
./sandbox up
```
This will run the `sandbox` shell script with the default configuration. See the [Basic Configuration](#basic-configuration) for other options.


Note for Ubuntu: You may need to alias `docker` to `sudo docker` or follow the steps in https://docs.docker.com/install/linux/linux-postinstall so that a non-root user can user the command `docker`.

Run the test command for examples of how to interact with the environment:
```
./sandbox test
```


### Windows


Note: Be sure to use the latest version of Windows 10. Older versions may not work properly.

Note: While installing the following programs, several restarts may be required for windows to recognize the new software correctly.

#### Option 1: Using WSL 2
The [installation instructions](https://docs.docker.com/desktop/windows/install/) for Docker Desktop contain some of this but are repeated here.

1. In order to work with Docker Desktop on windows, a prerequisite is **WSL2** and [install instructions are available here](https://docs.microsoft.com/en-us/windows/wsl/install).
2. Install **Docker Desktop** using the [instructions available here](https://docs.docker.com/desktop/windows/install/).
3. We recommend using the official Windows Terminal, [available in the app store here](https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701).
4. Install whatever distribution of Linux desired. 
5. Open the Windows Terminal with the distribution installed in the previous step and follow the instruction for Ubuntu and macOS above.

#### Option 2: Using Git for Windows/ MSYS 2

1. Install Git for Windows: https://gitforwindows.org/
2. Install and launch Docker for Windows: https://docs.docker.com/get-docker
3. Open "Git Bash" and follow the instruction for Ubuntu and macOS above, in the "Git Bash" terminal.

##### Troubleshooting

* If you see 
  ```plain
  the input device is not a TTY. If you are using mintty, try prefixing the command with 'winpty'.
  ```
  check that you are using the latest versions of: Docker, Git for Windows, and Windows 10.

  If this does not solve the issue, [open an issue](https://github.com/algorand/sandbox/issues) with all the versions with all the software used, as well as all the commands typed.

* If you see
  ```plain
  Error response from daemon: open \\.\pipe\docker_engine_linux: The system cannot find the file specified.
  ```
  check that Docker is running.


## Basic Configuration 

Sandbox supports two primary modes of operation. By default, a [private network](#private-network) will be created, which is only available from the local environment. There are also configurations available for the [public networks](#public-network) which will attempt to connect to one of the long running Algorand networks and allow interaction with it.


To specify which configuration to run:
```sh
./sandbox up $CONFIG
```

Where `$CONFIG` is specified as one of the configurations in the sandbox directory. 

For example to run a `dev` mode network, run:
```sh
./sandbox up dev
```

To switch the configuration:
```sh
./sandbox down
./sandbox clean
./sandbox up $NEW_CONFIG
```

### Private Network

If no configuration is specified the sandbox will be started with the `release` configuration which is a private network.  The other private network configurations are those not suffixed with `net`. Namely these are `beta`, `dev` and `nightly`. 

The private network environment creates and funds a number of accounts in the algod containers local `kmd` ready to use for testing transactions. These accounts can be reviewed using `./sandbox goal account list`. 

Private networks also include an `Indexer` service configured to synchronize against the private network. Because it doesn't require catching up to one of the long running networks it also starts very quickly.

The `dev` configuration runs a private network in dev mode. In this mode, every transaction being sent to the node automatically generates a new block, rather than wait for a new round in real time.  This is extremely useful for fast e2e testing of an application. 

### Public Network

The `mainnet`, `testnet`, `betanet`, and `devnet` configurations configure the sandbox to connect to one of those long running networks. Once started it will automatically attempt to catchup to the latest round. Catchup tends to take a while and a progress bar will be displayed to illustrate of the progress.

Due to technical limitations, this configuration does not contain preconfigured accounts that may be immediately transact with, and Indexer is not available. A new wallet and accounts may be created or imported at will using the [goal wallet new](https://developer.algorand.org/docs/clis/goal/wallet/new/) command to create a wallet and the [goal account import](https://developer.algorand.org/docs/clis/goal/account/import/) or [goal account new](https://developer.algorand.org/docs/clis/goal/account/new/) commands. 

_Note_
A newly created account will not be funded and wont be able to submit transactions until it is. If a `testnet` configuration is used, please visit the [TestNet Dispenser](https://bank.testnet.algorand.network/) to fund the newly created account.


## Advanced configurations

The sandbox environment is completely configured using the `config.*` files in the root of this repository. For example, the default configuration for **config.nightly** is:
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

The **up** command looks for the config extension based on the argument provided. With a custom configuration pointed to a fork, the sandbox will start using the fork:
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

## Working with files

Some Algorand commands require using a file for the input. For example working with TEAL programs. In some other cases like working with Logical signatures or transactions offline the output from a LogicSig or transaction may be needed. 

To stage a file use the `copyTo` command. The file will be placed in the algod data directory, which is where sandbox executes `goal`. This means the files can be used without specifying their full path.

To copy a file from sandbox (algod instance) use the `copyFrom` command. The file will be copied to sandbox directory on host filesystem.

#### copyTo example: 

these commands will stage two TEAL programs then use them in a `goal` command:
```sh
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


## Debugging for teal developers

For detailed information on how to debug smart contracts and use tealdbg CLI,please consult with [Algorand Development Portal :: Smart Contract Debugging](https://developer.algorand.org/docs/features/asc1/debugging/#setting-the-debugger-context).

Algorand smart contract debugging process uses `tealdbg` command line of algod instance(algod container in sandbox).

**Note**: Always use `tealdbg` with `--listen 0.0.0.0` or `--listen [IP ADDRESS]` flags, if access is needed to tealdbg from outside of algod docker container!

#### tealdbg examples:

Debugging smart contract with Chrome Developer Tools (CDT):
```~$ ./sandbox tealdbg debug ${TEAL_PROGRAM} -f cdt -d dryrun.json```

Debugging smart contract with Web Interface (primal web UI)
```~$ ./sandbox tealdbg debug ${TEAL_PROGRAM} -f web -d dryrun.json```
  
The debugging endpoint port (default 9392) is forwarded directly to the host machine and can be used directly by Chrome Dev Tools for debugging Algorand TEAL smart comtracts (Goto url chrome://inspect/ and configure port 9392 before using please).

Note: If a different port is needed than the default, it may be changed by running `tealdbg --port YOUR_PORT` then modifying the docker-compose.yml file and change all occurances of mapped 9392 port with the desired one.

## Errors

If something goes wrong, check the `sandbox.log` file for details.
