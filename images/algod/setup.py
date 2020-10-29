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

parser = argparse.ArgumentParser(description='Install, configure, and start algod.')

# Shared parameters
base_parser = argparse.ArgumentParser(add_help=False)
base_parser.add_argument('--bin-dir', required=True, help='Location to install algod binaries.')

subparsers = parser.add_subparsers()

configure = subparsers.add_parser('configure', parents=[base_parser], help='Configure private network for SDK.')
configure.add_argument('--network-template', required=True, help='Path to private network template file.')
configure.add_argument('--network-token', required=True, help='Valid token to use for algod/kmd.')
configure.add_argument('--algod-port', required=True, help='Port to use for algod.')
configure.add_argument('--kmd-port', required=True, help='Port to use for kmd.')
configure.add_argument('--network-dir', required=True, help='Path to create network.')
configure.add_argument('--bootstrap-url', required=True, help='DNS Bootstrap URL, empty for private networks.')
configure.add_argument('--genesis-file', required=True, help='Genesis file used by the network.')

start = subparsers.add_parser('start', parents=[base_parser], help='Start the network.')
start.add_argument('--network-dir', required=True, help='Path to create network.')

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

    return data_dir, kmd_dir


def write_start_script(network_dir, commands):
    with open(join(network_dir, 'start.sh'), 'w') as f:
        f.writelines(commands)


def create_real_network(bin_dir, network_dir, template, genesis_file):
    print("Setting up real retwork.")
    data_dir_src=join(bin_dir, 'data')
    target=join(network_dir, 'Node')

    # Reset in case it exists
    if os.path.exists(target):
        shutil.rmtree(target)

    # We have a blank data directory from the initial install script.
    shutil.copytree(data_dir_src, target)

    # Copy in the genesis file...
    shutil.copy(genesis_file, target)

    data_dir, kmd_dir = algod_directories(network_dir)
    write_start_script(network_dir, [
            '%s/goal node start -d %s\n' % (bin_dir, data_dir),
            '%s/kmd start -t 0 -d %s\n' % (bin_dir, kmd_dir),
            'sleep infinity\n'
        ])


def create_private_network(bin_dir, network_dir, template):
    """
    Create a private network.
    """
    print("Creating a private network.")
    # Reset network dir before creating a new one.
    if os.path.exists(args.network_dir):
        shutil.rmtree(args.network_dir)

    # $BIN_DIR/goal network create -n testnetwork -r $NETWORK_DIR -t network_config/$TEMPLATE
    subprocess.check_call(['%s/goal network create -n testnetwork -r %s -t %s' % (bin_dir, network_dir, template)], shell=True)

    data_dir, kmd_dir = algod_directories(network_dir)

    write_start_script(network_dir, [
            '%s/goal network start -r %s\n' % (bin_dir, network_dir),
            '%s/kmd start -t 0 -d %s\n' % (bin_dir, kmd_dir),
            'sleep infinity\n'
        ])


def configure_data_dir(network_dir, token, algod_port, kmd_port, bootstrap_url):
    node_dir, kmd_dir = algod_directories(network_dir)

    # Set tokens
    with open(join(node_dir, 'algod.token'), 'w') as f:
        f.write(token)
    with open(join(kmd_dir, 'kmd.token'), 'w') as f:
        f.write(token)

    # Setup config, inject port
    with open(join(node_dir, 'config.json'), 'w') as f:
        f.write('{ "GossipFanout": 1, "EndpointAddress": "0.0.0.0:%s", "DNSBootstrapID": "%s", "IncomingConnectionsLimit": 0, "Archival":false, "isIndexerActive":false, "EnableDeveloperAPI":true}' % (algod_port, bootstrap_url))
    with open(join(kmd_dir, 'kmd_config.json'), 'w') as f:
        f.write('{  "address":"0.0.0.0:%s",  "allowed_origins":["*"]}' % kmd_port)


def configure_handler(args):
    """
    configure subcommand - configure a private network using the installed binaries.
    """
    if args.genesis_file == None or args.genesis_file == "" or os.path.isdir(args.genesis_file):
        create_private_network(args.bin_dir, args.network_dir, args.network_template)
    else:
        create_real_network(args.bin_dir, args.network_dir, args.network_template, args.genesis_file)

    configure_data_dir(args.network_dir, args.network_token, args.algod_port, args.kmd_port, args.bootstrap_url)


def start_handler(args):
    """
    start subcommand - start algod + kmd using start script created during setup.
    """
    subprocess.check_call(['bash %s/start.sh' % args.network_dir], shell=True)


if __name__ == '__main__':
    configure.set_defaults(func=configure_handler)
    start.set_defaults(func=start_handler)
    args = parser.parse_args()

    print("Running algod helper script with the following arguments:")
    pp.pprint(vars(args))

    args.func(args)
