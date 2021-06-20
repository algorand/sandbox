import pytest

from algosdk.error import AlgodHTTPError
from algosdk.future.transaction import AssetConfigTxn
from fixtures import *


def test_issue_tasa_success(accounts, algodclient, algod_params, algorand_test_helper, logger):
    # Get issuer algorand account, with public and secret keys.
    issuer_account = accounts.get_issuer_account()
    logger.debug("Issuer address: {}".format(issuer_account["pk"]))

    # TASA creation transaction.
    # TODO(ad): Replace with library function.
    txn = AssetConfigTxn(
        sender=issuer_account["pk"],
        sp=algod_params,
        total=1,
        default_frozen=False,
        unit_name="TICKET",
        asset_name="ticket",
        manager=issuer_account["pk"],
        reserve=issuer_account["pk"],
        freeze=issuer_account["pk"],
        clawback=issuer_account["pk"],
        url="https://test/ticket/details", 
        decimals=0)

    # Sign with secret key of issuer
    stxn = txn.sign(issuer_account["sk"])

    # Send the TASA creation transaction to the network and retrieve the txid.
    txid = algodclient.send_transaction(stxn)
    logger.debug("TASA create txn Id: {}".format(txid))

    # Wait for the transaction to be confirmed.
    algorand_test_helper.wait_for_confirmation(txid)

    # Retrieve the asset ID of the newly created asset from the transaction.
    ptx = algodclient.pending_transaction_info(txid)
    asset_id = ptx["asset-index"]

    # Fetch the new asset's information from the issuer account and log.
    algorand_test_helper.log_created_asset(issuer_account["pk"], asset_id)
    algorand_test_helper.log_asset_holding(issuer_account["pk"], asset_id)


def test_spoof_issue_tasa_fail(accounts, algodclient, algod_params, algorand_test_helper, logger):
    # Get issuer's public key (Secret key is not available to anyone else,
    # inlcuding the fraudster).
    issuer_pk = accounts.get_issuer_account()["pk"]
    logger.debug("Issuer address: {}".format(issuer_pk))

    # Get fraudster algorand account, with public and secret keys.
    fraudster_account = accounts.get_fraudster_account()
    logger.debug("Fraudster address: {}".format(fraudster_account["pk"]))

    # Spoofed TASA creation transaction with issuer info.
    # TODO(ad): Replace with library function.
    txn = AssetConfigTxn(
        sender=issuer_pk,
        sp=algod_params,
        total=1,
        default_frozen=False,
        unit_name="FTICKET",
        asset_name="fticket",
        manager=issuer_pk,
        reserve=issuer_pk,
        freeze=issuer_pk,
        clawback=issuer_pk,
        url="https://test/fticket/details", 
        decimals=0)

    # Sign with secret key of fraudster (the only secret key accessible by the
    # fraudster).
    stxn = txn.sign(fraudster_account["sk"])

    # TASA creation transaction will be rejected by the network. 
    with pytest.raises(AlgodHTTPError):
        algodclient.send_transaction(stxn)
