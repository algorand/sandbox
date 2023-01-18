# Algorand Sandbox

This is a fast way to create and configure an Algorand development environment with [Algod](https://github.com/algorand/go-algorand) and [Indexer](https://github.com/algorand/indexer).

**Docker Compose** _MUST_ be installed. [Instructions](https://docs.docker.com/compose/install/).

On a _Windows_ machine, **Docker Desktop** comes with the necessary tools. Please see the [Windows](#windows) section in getting started for more details.

**Warning**: Algorand Sandbox is _not_ meant for production environments and should _not_ be used to store secure Algorand keys. Updates may reset all the data and keys that are stored.

## Usage

Use the **sandbox** command to interact with the Algorand Sandbox.

```plain
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

- `algod`:
  - address: `http://localhost:4001`
  - token: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`
- `kmd`:
  - address: `http://localhost:4002`
  - token: `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`
- `indexer`:
  - address: `http://localhost:8980`

## Getting Started

### Ubuntu and macOS

Make sure the docker daemon is running and docker-compose is installed.

Open a terminal and run:

```bash
git clone https://github.com/algorand/sandbox.git
```

In whatever local directory the sandbox should reside. Then:

```bash
cd sandbox
./sandbox up
```

This will run the `sandbox` shell script with the default configuration. See the [Basic Configuration](#basic-configuration) for other options.

<!-- markdownlint-disable-file MD034 -->

Note for Ubuntu: You may need to alias `docker` to `sudo docker` or follow the steps in https://docs.docker.com/install/linux/linux-postinstall so that a non-root user can use the command `docker`.

Run the test command for examples of how to interact with the environment:

```bash
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

**Tip**: If you are using VSCode, do not forget to use the WSL2 terminal inside VSCode too. You may follow [this Microsoft tutorial](https://learn.microsoft.com/en-us/windows/wsl/tutorials/wsl-vscode).

#### Option 2: Using Git for Windows/ MSYS 2 (not recommended)

This option is not fully tested and may cause issues.
It is recommended to use WSL 2.

1. Install Git for Windows: https://gitforwindows.org/
2. Install and launch Docker for Windows: https://docs.docker.com/get-docker
3. Open "Git Bash" and follow the instruction for Ubuntu and macOS above, in the "Git Bash" terminal.

##### Troubleshooting

- If you see

  ```plain
  the input device is not a TTY. If you are using mintty, try prefixing the command with 'winpty'.
  ```

  check that you are using the latest versions of: Docker, Git for Windows, and Windows 10.

  If this does not solve the issue, [open an issue](https://github.com/algorand/sandbox/issues) with all the versions with all the software used, as well as all the commands typed.

- If you see

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

If no configuration is specified the sandbox will be started with the `release` configuration which is a private network. The other private network configurations are those not suffixed with `net`. Namely these are `beta`, `dev` and `nightly`.

The private network environment creates and funds a number of accounts in the algod containers local `kmd` ready to use for testing transactions. These accounts can be reviewed using `./sandbox goal account list`.

Private networks also include an `Indexer` service configured to synchronize against the private network. Because it doesn't require catching up to one of the long running networks it also starts very quickly.

The `dev` configuration starts a private network using the latest release with these algod configuration customizations:
* `"DevMode": true` - In dev mode, every transaction being sent to the node automatically generates a new block, rather than wait for a new round in real time. This is extremely useful for fast e2e testing of an application.
* `"RewardsPoolBalance": 0` - Prevents participation rewards by overriding the initial rewards pool balance.  In a variety of test scenarios, participation rewards obscure testing Algo balances.

It takes a long time to generate participation keys, so the default configurations use the `NETWORK_NUM_ROUNDS` parameter to limit how many are created. Unless the default value is changed, the network will stall after 24 hours. Some configurations have been changed so that they can be run for over a week. Review the setting to make sure it is suitable for how you would like to use the sandbox.

### Public Network

The `mainnet`, `testnet`, `betanet`, and `devnet` configurations configure the sandbox to connect to one of those long running networks. Once started it will automatically attempt to catchup to the latest round. Catchup tends to take a while and a progress bar will be displayed to illustrate of the progress.

Due to technical limitations, this configuration does not contain preconfigured accounts that may be immediately transact with, and Indexer is not available. A new wallet and accounts may be created or imported at will using the [goal wallet new](https://developer.algorand.org/docs/clis/goal/wallet/new/) command to create a wallet and the [goal account import](https://developer.algorand.org/docs/clis/goal/account/import/) or [goal account new](https://developer.algorand.org/docs/clis/goal/account/new/) commands.

_Note_
A newly created account will not be funded and wont be able to submit transactions until it is. If a `testnet` configuration is used, please visit the [TestNet Dispenser](https://bank.testnet.algorand.network/) to fund the newly created account.

## Advanced configurations

The sandbox environment is completely configured using the `config.*` files in the root of this repository. For example, the default configuration for **config.nightly** is:

```bash
export ALGOD_CHANNEL="nightly"
export ALGOD_URL=""
export ALGOD_BRANCH=""
export ALGOD_SHA=""
export NETWORK=""
export NETWORK_TEMPLATE="images/algod/future_template.json"
export NETWORK_NUM_ROUNDS=300000
export NETWORK_BOOTSTRAP_URL=""
export NETWORK_GENESIS_FILE=""
export NODE_ARCHIVAL=""
export INDEXER_URL="https://github.com/algorand/indexer"
export INDEXER_BRANCH="develop"
export INDEXER_SHA=""
export INDEXER_DISABLED=""
export INDEXER_ENABLE_ALL_PARAMETERS="false"
```

Indexer is always built from source since it can be done quickly. For most configurations, algod will be installed using our standard release channels, but building from source is also available by setting the git URL, Branch and optionally a specific SHA commit hash.

The **up** command looks for the config extension based on the argument provided. With a custom configuration pointed to a fork, the sandbox will start using the fork:

```bash
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
export INDEXER_ENABLE_ALL_PARAMETERS="false"
```

### Indexer Query Parameters

By default Indexer disables many query parameters which are known to have performance problems without specially configured databases. You can identify these parameters if your Indexer calls return a response like the following:
```
{"message":"provided disabled parameter: tx-type"}
```

To override the disabled parameters and enable everything, add the following to your `config.<name>` file:
```
export INDEXER_ENABLE_ALL_PARAMETERS="true"
```

## Working with files

Some Algorand commands require using a file for the input. For example working with TEAL programs. In some other cases like working with Logical signatures or transactions offline the output from a LogicSig or transaction may be needed.

To stage a file use the `copyTo` command. The file will be placed in the algod data directory, which is where sandbox executes `goal`. This means the files can be used without specifying their full path.

To copy a file from sandbox (algod instance) use the `copyFrom` command. The file will be copied to sandbox directory on host filesystem.

### copyTo example

these commands will stage two TEAL programs then use them in a `goal` command:

```sh
~$ ./sandbox copyTo approval.teal
~$ ./sandbox copyTo clear.teal
~$ ./sandbox goal app create --approval-prog approval.teal --clear-prog clear.teal --creator YOUR_ACCOUNT  --global-byteslices 1 --global-ints 1 --local-byteslices 1 --local-ints 1
```

### copyFrom example

these commands will create and copy a signed logic transaction file, created by `goal`, to be sent or communicated off the chain (e.g. by email or as a QR Code) and submitted else where:

```bash
~$ ./sandbox goal clerk send -f <source-account> -t <destination-account> --fee 1000 -a 1000000 -o "unsigned.txn"
~$ ./sandbox goal clerk sign --infile unsigned.txn --outfile signed.txn
~$ ./sandbox copyFrom "signed.txn"
```

## Errors

If something goes wrong, check the `sandbox.log` file for details.

## Debugging for teal developers

For detailed information on how to debug smart contracts and use tealdbg CLI,please consult with [Algorand Development Portal :: Debugging smart contracts](https://developer.algorand.org/docs/get-details/dapps/smart-contracts/debugging/).

Algorand smart contract debugging process uses `tealdbg` command line of algod instance(algod container in sandbox).

**Note**: Always use `tealdbg` with `--listen 0.0.0.0` or `--listen [IP ADDRESS]` flags, if access is needed to tealdbg from outside of algod docker container!

### tealdbg examples

Debugging smart contract with Chrome Developer Tools (CDT):
`~$ ./sandbox tealdbg debug ${TEAL_PROGRAM} -f cdt -d dryrun.json`

Debugging smart contract with Web Interface (primal web UI)
`~$ ./sandbox tealdbg debug ${TEAL_PROGRAM} -f web -d dryrun.json`

The debugging endpoint port (default 9392) is forwarded directly to the host machine and can be used directly by Chrome Dev Tools for debugging Algorand TEAL smart comtracts (Goto url chrome://inspect/ and configure port 9392 before using please).

Note: If a different port is needed than the default, it may be changed by running `tealdbg --port YOUR_PORT` then modifying the docker-compose.yml file and change all occurances of mapped 9392 port with the desired one.

## ADVANCED: Sandbox Interactive Debugging with VSCode's `Remote - Container` Extension

For those looking to develop or extend **algod** or **indexer** it's highly recommended to test and debug using a realistic environment. Being able to interactively debug code with breakpoints and introspect the stack as the Algorand daemon communicates with a live network is quite useful. Here are steps that you can take if you want to run an interactive debugger with an `indexer` running on the sandbox. Analogous instructions work for `algod` as well.

Before starting, make sure you have VS-Code and have installed the [Remote - Containers Extension](https://code.visualstudio.com/docs/remote/containers-tutorial).

1. Inside [docker_compose.yml](./docker-compose.yml) add the key/val `privileged: true` under the `indexer:` service
2. Start the sandbox with `./sandbox up YOUR_CONFIG` and wait for it to be fully up and running

- you may need to run a `./sandbox clean` first
- you can verify by seeing healthy output from `./sandbox test`
<!-- markdownlint-disable-file MD029 -->

3. In VS Code...
4. Go to the [Command Palette](https://code.visualstudio.com/docs/getstarted/tips-and-tricks#_command-palette) (on a Mac it's **SHIFT-COMMAND-P**) and enter `Remote - Containers: Attach to Running Container`
5. The container of interest, e.g. `/algorand-sandbox-indexer`, should pop up and you should choose it
6. The first time you attach to a container, you'll get the option of choosing which top-level directory _inside the container_ to attach the file browser to. The default HOME (`/opt/indexer` in the case of indexer) is usually your best choice
7. Next, VS Code should auto-detect that you're running a `go` based project and suggest various extensions to add into the container enviroment. You should do this
8. Now navigate to the file you'd like to debug (e.g. `api/handlers.go`) and add a breakpoint as you usually would
9. You'll need to identify the PID of the indexer process so you can attach to it. Choose **Terminal** &rarr; **New Terminal** from the menu and run `ps | egrep "daemon|PID"`. Note the resulting PID
10. Now start the debugger with `F5`. It should give you the option to `attach to a process` and generate a `launch.json` with `processId: 0` for you
11. Modify the `launch.json` with the correct `processId`. Below I provide an example of a `launch.json`
12. Now you're ready to rumble! If you hit your sandbox endpoint with a well formatted request, you should end up reaching and pausing at your break point. For **indexer**, you would request against port 8980. See the `curl` example below

### Example `launch.json`

```json
{
  // Use IntelliSense to learn about possible attributes.
  // Hover to view descriptions of existing attributes.
  // For more information, visit: https://go.microsoft.com/fwlink/?linkid=830387
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to Process",
      "type": "go",
      "request": "attach",
      "mode": "local",
      "processId": YOUR_PID_HERE
    }
  ]
}
```

### Example `curl` command

```bash
~$ curl "localhost:8980/v2/accounts"
```

## Deep technical details

### About pseudo-TTY issues or why do we use the `-T` flag in `dc exec -T` everywhere?

Windows Msys / Git Bash does not have a pseudo-TTY.
Because of that, any time a command requires a pseudo-TTY, it fails with error:

  ```plain
  the input device is not a TTY. If you are using mintty, try prefixing the command with 'winpty'.
  ```

Unfortunately prefixing all commands with `winpty` is not an option because `winpty` will break when piping or using command substitution (\`...\` and `$()`).
The adopted solution is to use a pseudo-TTY only when absolutely required, that is when executing an interactive command such as `bash` inside `docker`.

See comments around the commands `dc` and `dc_pty` in the file `sandbox`.
