"""
Successfully creates a TASA from an issuer account and attempts to spoof the
origination of a TASA from an issuer through a fraudster account, which results
in the ASA creation txn being rejected.

Requirements:
    Running private Algorand network accessible through algod_address with
    algod_token. Assumes network is provisioned with accounts corresponding to
    each mnemonic stored in mnemonics. If using algorand-sandbox, these
    mnemonics correspond to the accounts provisioned by the default private
    network, which can be launched using,

    /path/to/sandbox/binary up 

Usage:
    python3 test_spoof_create_tasa.py    
"""

import json

from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn

TOKETMASTER_IDX = 0
ISSUER_IDX = 1
FRAUDSTER_IDX = 2

print("Creating accounts...\n")

# Accounts corresponding to these mnemonics must already be setup on the 
# network. If using algorand-sandbox, these mnemonics correspond to the accounts
# provisioned by the default private network. 
mnemonics = [
    "kingdom social feel raw primary lab shallow winner remind empty sing believe beef chunk lizard mesh town female web awesome vacant pond giggle absent prefer",
    "okay today prevent few hill step climb jazz combine soul staff butter boil else key file fade come friend abandon river basket nest about kit",
    "orient destroy edge grit climb scan super always capable visa orange web car reduce fee aspect mosquito enroll crane impulse crawl warrior remove abstract kite"
    ]

# For ease of reference, adding the account public and private keys to an
# accounts dict.
accounts = []
for m in mnemonics:
    a = {}
    a['pk'] = mnemonic.to_public_key(m)
    a['sk'] = mnemonic.to_private_key(m)
    accounts.append(a)

# Initialize an algod client
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)

print("Toketmaster address: {}".format(accounts[TOKETMASTER_IDX]["pk"]))
print("Toketmaster account balance: {}".format(algod_client.account_info(accounts[TOKETMASTER_IDX]["pk"])["amount"]))
print("Issuer address: {}".format(accounts[ISSUER_IDX]["pk"]))
print("Issuer account balance: {}".format(algod_client.account_info(accounts[ISSUER_IDX]["pk"])["amount"]))
print("Fraudster address: {}".format(accounts[FRAUDSTER_IDX]["pk"]))
print("Fraudster account balance: {}".format(algod_client.account_info(accounts[FRAUDSTER_IDX]["pk"])["amount"]))

# Methods copied from https://github.com/algorand/docs/blob/master/examples/assets/v2/python/asset_example.py.

def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo

# Utility function used to print created asset for account and assetid
def print_created_asset(algodclient, account, assetid):    
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then use 'account_info['created-assets'][0] to get info on the created asset
    account_info = algodclient.account_info(account)
    idx = 0;
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1       
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break

# Utility function used to print asset holding for account and assetid
def print_asset_holding(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1        
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break

# Get network params for transactions before every transaction.
params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
params.fee = 1000
params.flat_fee = True

print("\nIssuer creating TASA...\n")

# Issuer creates an asset called 'ticket' and sets itself as the manager,
# reserve, freeze, and clawback address.
# Asset Creation transaction
txn = AssetConfigTxn(
    sender=accounts[ISSUER_IDX]["pk"],
    sp=params,
    total=1,
    default_frozen=False,
    unit_name="TICKET",
    asset_name="ticket",
    manager=accounts[ISSUER_IDX]["pk"],
    reserve=accounts[ISSUER_IDX]["pk"],
    freeze=accounts[ISSUER_IDX]["pk"],
    clawback=accounts[ISSUER_IDX]["pk"],
    url="https://path/to/ticket/details", 
    decimals=0)

# Sign with secret key of issuer
stxn = txn.sign(accounts[ISSUER_IDX]["sk"])

# Send the transaction to the network and retrieve the txid.
txid = algod_client.send_transaction(stxn)
print("TASA create txn Id: {}".format(txid))

# Retrieve the asset ID of the newly created asset by first
# ensuring that the creation transaction was confirmed,
# then grabbing the asset id from the transaction.

# Wait for the transaction to be confirmed
wait_for_confirmation(algod_client,txid)

try:
    # Pull account info for the issuer
    # account_info = algod_client.account_info(accounts[1]['pk'])
    # get asset_id from tx
    # Get the new asset's information from the issuer account
    ptx = algod_client.pending_transaction_info(txid)
    asset_id = ptx["asset-index"]
    print_created_asset(algod_client, accounts[ISSUER_IDX]['pk'], asset_id)
    print_asset_holding(algod_client, accounts[ISSUER_IDX]['pk'], asset_id)
except Exception as e:
    print(e)

print("\nFraudster creating TASA from issuer...\n")

txn = AssetConfigTxn(
    sender=accounts[ISSUER_IDX]["pk"],
    sp=params,
    total=1,
    default_frozen=False,
    unit_name="FTICKET",
    asset_name="fticket",
    manager=accounts[ISSUER_IDX]["pk"],
    reserve=accounts[ISSUER_IDX]["pk"],
    freeze=accounts[ISSUER_IDX]["pk"],
    clawback=accounts[ISSUER_IDX]["pk"],
    url="https://path/to/f/ticket/details", 
    decimals=0)

try:
    # Sign with secret key of fraudster
    stxn = txn.sign(accounts[FRAUDSTER_IDX]["sk"])

    # Sent transaction to the network should be rejected.
    algod_client.send_transaction(stxn)
except Exception as e:
    print("FAILED: {}".format(e))