from algosdk.v2client import algod, indexer


_algod_token = "LGlsGlaSiY37Y3xKQly071AsDwS6PeP73mAaFJLF"
_headers = {
        "X-API-Key": _algod_token,
    }


algod_client = algod.AlgodClient(
    algod_token=_algod_token, 
    algod_address="https://testnet-algorand.api.purestake.io/ps2",
    headers=_headers)


indexer_client = indexer.IndexerClient(
    indexer_token=_algod_token, 
    indexer_address="https://testnet-algorand.api.purestake.io/idx2", 
    headers=_headers)
