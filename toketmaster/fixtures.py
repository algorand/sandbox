import logging
import pytest

from algosdk.v2client import algod

from algorand_test_helper import AlgorandTestHelper
from private_network_accounts import PrivateNetworkAccounts


logging.basicConfig(format="%(asctime)s %(message)s")


@pytest.fixture(scope="module")
def accounts():
    return PrivateNetworkAccounts()


@pytest.fixture(scope="module")
def algodclient():
    # TODO(hv): Grab from env vars
    algod_address = "http://localhost:4001"
    algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
    return algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)
    

@pytest.fixture(scope="module")
def algod_params(algodclient):
	# Set network params for transactions.
	params = algodclient.suggested_params()
	params.fee = 1000
	params.flat_fee = True
	return params


@pytest.fixture(scope="module")
def logger():
	l = logging.getLogger()
	l.setLevel(logging.DEBUG)
	return l


@pytest.fixture(scope="module")
def algorand_test_helper(algodclient, logger):
	return AlgorandTestHelper(algodclient, logger)
