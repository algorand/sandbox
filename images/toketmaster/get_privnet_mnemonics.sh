#!/bin/bash

# Fetch Algorand private network account mnemonics and store in file.
#
# Configured with environment variables:
#   MNEMONICS_FILE - Path to output file storing mnemomics.
set -e

# Fetch account addresses.
accounts=$(goal account list | awk '{print $2}')

# Fetch mnemonic for each account and store in file.
for a in $accounts;
do
	goal account export -a $a | awk -F "\"" '{print $2}' >> ${MNEMONICS_FILE};
done
