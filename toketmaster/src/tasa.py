import time
from typing import Optional

from algosdk import transaction
from algosdk.error import IndexerHTTPError

from toketmaster.src.client import algod_client, indexer_client
from toketmaster.src.models import Wallet


def create_tasa(creator: Wallet,
                fee: int,
                unit_name: str,
                asset_name: str,
                url: str,
                default_frozen: bool = False,
                decimals: int = 0,
                manager: Optional[Wallet] = None,
                reserve: Optional[Wallet] = None,
                freeze: Optional[Wallet] = None,
                clawback: Optional[Wallet] = None,
                ) -> str:
    params = algod_client.suggested_params()
    
    # create TASA
    txn = transaction.AssetConfigTxn(
        sender=creator.public_key,
        first=params.first,
        last=params.last,
        gh=params.gh,
        fee=fee,
        total=1,
        default_frozen=default_frozen,
        unit_name=unit_name,
        asset_name=asset_name,
        manager=None if manager is None else manager.public_key,
        reserve=None if reserve is None else reserve.public_key,
        freeze=None if freeze is None else freeze.public_key,
        clawback=None if clawback is None else clawback.public_key,
        url=url,
        decimals=decimals
    )
    # TM signs the TASA for ITO
    signed_tx = txn.sign(private_key=creator.secret_key)
    
    # Publish the TASA
    txid = algod_client.send_transaction(signed_tx)
    
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