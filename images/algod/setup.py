#!/usr/bin/env python3

# Script to help configure and run different algorand configurations.
# Notably this script can configure an algorand installation to run as a
# private network, or as a node connected to a long-running network.
#
# For parameter information run with './setup.py -h'
#
# Parameter error handling is not great with this script. It wont complain
# if you provide arguments unused parameters.

import argparse
import os
import pprint
import shutil
import subprocess
import tarfile
import time
import json
import urllib.request
from os.path import expanduser, join

from typing import List

parser = argparse.ArgumentParser(description='''\
        Configure private network for SDK and prepare it to run. A start script and
        symlink to data directory will be generated to make it easier to use.''')
parser.add_argument('--bin-dir', required=True, help='Location to install algod binaries.')
parser.add_argument('--data-dir', required=True, help='Location to place a symlink to the data directory.')
parser.add_argument('--start-script', required=True, help='Path to start script, including the script name.')
parser.add_argument('--network-template', required=True, help='Path to private network template file.')
parser.add_argument('--network-token', required=True, help='Valid token to use for algod/kmd.')
parser.add_argument('--algod-port', required=True, help='Port to use for algod.')
parser.add_argument('--kmd-port', required=True, help='Port to use for kmd.')
parser.add_argument('--network-dir', required=True, help='Path to create network.')
parser.add_argument('--bootstrap-url', required=True, help='DNS Bootstrap URL, empty for private networks.')
parser.add_argument('--genesis-file', required=True, help='Genesis file used by the network.')
parser.add_argument('--archival', type=bool, default=False, help='When True, bootstrap an archival node.')
parser.add_argument('--max-account-lookback', required=True, help='Max account lookback range for account states on the node.')

pp = pprint.PrettyPrinter(indent=4)


def algod_directories(network_dir):
    """
    Compute data/kmd directories.
    """
    data_dir=join(network_dir, 'Node')

    kmd_dir = None
    options = [filename for filename in os.listdir(data_dir) if filename.startswith('kmd')]

    # When setting up the real network the kmd dir doesn't exist yet because algod hasn't been started.
    if len(options) == 0:
        kmd_dir=join(data_dir, 'kmd-v0.5')
        os.mkdir(kmd_dir)
    else:
        kmd_dir=join(data_dir, options[0])

    follower_dir=join(network_dir, 'Follower')

    return data_dir, kmd_dir, follower_dir


def create_real_network(bin_dir, network_dir, template, genesis_file) -> List[str]:
    data_dir_src=join(bin_dir, 'data')
    target=join(network_dir, 'Node')

    # Reset in case it exists
    if os.path.exists(target):
        shutil.rmtree(target)
    os.makedirs(target, exist_ok=True)

    # Copy in the genesis file...
    shutil.copy(genesis_file, target)

    data_dir, kmd_dir, _ = algod_directories(network_dir)

    return ['%s/goal node start -d %s' % (bin_dir, data_dir),
            '%s/kmd start -t 0 -d %s' % (bin_dir, kmd_dir)]


def create_private_network(bin_dir, network_dir, template) -> List[str]:
    """
    Create a private network.
    """
    # Reset network dir before creating a new one.
    if os.path.exists(args.network_dir):
        shutil.rmtree(args.network_dir)

    # Use goal to create the private network.
    subprocess.check_call(['%s/goal network create -n sandnet -r %s -t %s' % (bin_dir, network_dir, template)], shell=True)

    _, kmd_dir, _ = algod_directories(network_dir)
    return ['%s/goal network start -r %s' % (bin_dir, network_dir),
            '%s/kmd start -t 0 -d %s' % (bin_dir, kmd_dir)]


def configure_data_dir(network_dir, token, algod_port, kmd_port, bootstrap_url, archival, max_account_lookback):
    node_dir, kmd_dir, follower_dir = algod_directories(network_dir)

    has_follower = os.path.exists(follower_dir)

    # Set tokens
    with open(join(node_dir, 'algod.token'), 'w') as f:
        f.write(token)
    with open(join(node_dir, 'algod.admin.token'), 'w') as f:
        f.write(token)
    if has_follower:
        with open(join(follower_dir, 'algod.token'), 'w') as f:
            f.write(token)
        with open(join(follower_dir, 'algod.admin.token'), 'w') as f:
            f.write(token)
    with open(join(kmd_dir, 'kmd.token'), 'w') as f:
        f.write(token)

    # Setup config, inject port
    node_config_path = join(node_dir, "config.json")
    archival = 'true' if archival else 'false'
    if has_follower:
        node_config = f'{{ "Version": 34, "GossipFanout": 1, "EndpointAddress": "0.0.0.0:{algod_port}", "EnablePrivateNetworkAccessHeader": true, "Archival":{archival}, "EnableDeveloperAPI":true, "NetAddress": "127.0.0.1:0", "DNSBootstrapID": "{bootstrap_url}", "EnableTxnEvalTracer": true, "MaxAcctLookback": {max_account_lookback}}}'
    else:
        node_config = f'{{ "Version": 34, "GossipFanout": 1, "EndpointAddress": "0.0.0.0:{algod_port}", "EnablePrivateNetworkAccessHeader": true, "DNSBootstrapID": "{bootstrap_url}", "IncomingConnectionsLimit": 0, "Archival":{archival}, "EnableDeveloperAPI":true, "EnableTxnEvalTracer": true, "MaxAcctLookback": {max_account_lookback}}}'
    print(f"writing to node_config_path=[{node_config_path}] config json: {node_config}")
    with open(node_config_path, "w") as f:
        f.write(node_config)

    kmd_config_path = join(kmd_dir, 'kmd_config.json')
    kmd_config = f'{{ "address":"0.0.0.0:{kmd_port}",  "allowed_origins":["*"], "allow_header_pna": true }}'
    print(f"writing to kmd_config_path=[{kmd_config_path}] config json: {kmd_config}")
    with open(kmd_config_path, 'w') as f:
        f.write(kmd_config)

if __name__ == '__main__':
    args = parser.parse_args()

    print('Configuring network with the following arguments:')
    pp.pprint(vars(args))


    # Setup network
    privateNetworkMode = args.genesis_file == None or args.genesis_file == '' or os.path.isdir(args.genesis_file)
    if privateNetworkMode:
        print('Creating a private network.')
        startCommands = create_private_network(args.bin_dir, args.network_dir, args.network_template)
    else:
        print('Setting up real retwork.')
        startCommands = create_real_network(args.bin_dir, args.network_dir, args.network_template, args.genesis_file)

    # Write start script
    print(f'Start commands for {args.start_script}:')
    pp.pprint(f'startCommands={startCommands}')
    with open(args.start_script, 'w') as f:
        f.write('#!/usr/bin/env bash\n')
        for line in startCommands:
            f.write(f'{line}\n')
        f.write('sleep infinity\n')
    os.chmod(args.start_script, 0o755)
    print(f"Finished preparing start script '{args.start_script}' under /opt/")

    # Create symlink
    data_dir, _, _ = algod_directories(args.network_dir)
    print(f'Creating symlink {args.data_dir} -> {data_dir}')
    os.symlink(data_dir, args.data_dir)

    # Configure network
    configure_data_dir(
        args.network_dir,
        args.network_token,
        args.algod_port,
        args.kmd_port,
        args.bootstrap_url,
        args.archival,
        args.max_account_lookback,
    )

