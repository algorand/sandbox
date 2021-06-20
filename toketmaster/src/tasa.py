from client import algod_client, indexer_client
from models import Wallet

from algosdk import transaction
from algosdk.error import IndexerHTTPError
import time


def create_tasa(**kwargs) -> str:
    params = algod_client.suggested_params()
    
    # create TASA
    txn = transaction.AssetConfigTxn(
        sender=kwargs['sender'],
        first=params.first,
        last=params.last,
        gh=params.gh,
        fee=kwargs['fee'],
        total=kwargs['total'],
        default_frozen=kwargs['default_frozen'],
        unit_name=kwargs['unit_name'],
        asset_name=kwargs['asset_name'],
        manager=kwargs['manager'],
        reserve=kwargs['reserve'],
        freeze=kwargs['freeze'],
        clawback=kwargs['clawback'],
        url=kwargs['url'],
        decimals=kwargs['decimals']
    )
    # TM signs the TASA for ITO
    stxn = txn.sign(private_key=kwargs['signing_key'])
    
    # Publish the TASA
    txid = algod_client.send_transaction(stxn)
    
    return txid


def get_tasa_id(tasa_create_txid: str) -> str:
    try:
        res = indexer_client.transaction(tasa_create_txid)  # wait for a few seconds if the transactions is not found
        
    except IndexerHTTPError:
        print('TASA Creation ID is not found. Waiting for 10 seconds, and retrying.')
        time.sleep(10)
        res = indexer_client.transaction(tasa_create_txid)
    
    # get the TASA index from the transaction
    tasa_index = res['transaction']['created-asset-index']
    
    return tasa_index


def transfer_tasa(from_: Wallet, to: Wallet, tasa_id: str, fee: int) -> str:
    # We need to opt in the client for the TASA transfer first
    params = algod_client.suggested_params()
    opt_in_transaction = transaction.AssetTransferTxn(
        sender=to.public_key,
        fee=0,
        first=params.first,
        last=params.last,
        gh=params.gh,
        receiver=to.public_key,
        amt=0,
        index=tasa_id,
    )
    stxn = opt_in_transaction.sign(to.secret_key)  # signed by the Client's key
    algod_client.send_transaction(stxn)
    
    # after the client opted-in for the TASA transfer
    # we can transfer the TASA
    tasa_transfer_transaction = transaction.AssetTransferTxn(
        sender=from_.public_key,
        fee=fee,  # not sure how this works yet
        flat_fee=True,
        first=params.first,
        last=params.last,
        gh=params.gh,
        receiver=to.public_key,
        amt=1,
        index=tasa_id,
    )

    stxn = tasa_transfer_transaction.sign(from_.secret_key)  # signed by the ToketMaster's key
    return algod_client.send_transaction(stxn)