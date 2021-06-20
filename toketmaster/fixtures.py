import logging
import os
import pytest

from algosdk.v2client import algod

from algorand_test_helper import AlgorandTestHelper
from network_accounts import NetworkAccounts


logging.basicConfig(format="%(asctime)s %(message)s")


# Environment variables for algod client.
_ALGOD_ADDRESS_ENVVAR = "ALGOD_ADDR"
_ALGOD_TOKEN_ENVVAR = "ALGOD_TOKEN"


@pytest.fixture(scope="module")
def accounts():
    return NetworkAccounts()


@pytest.fixture(scope="module")
def algodclient():
	if _ALGOD_ADDRESS_ENVVAR not in os.environ:
		raise ValueError("algod address environment variable '{}' not set".format(
			_ALGOD_ADDRESS_ENVVAR))

	if _ALGOD_TOKEN_ENVVAR not in os.environ:
		raise ValueError("algod token environment variable '{}' not set".format(
			ALGOD_TOKEN))

	algod_address = os.environ.get(_ALGOD_ADDRESS_ENVVAR)
	algod_token = os.environ.get(_ALGOD_TOKEN_ENVVAR)
	headers = {
		"X-API-Key": algod_token,
	}

	return algod.AlgodClient(
		algod_token=algod_token,
		algod_address=algod_address,
		headers=headers)
    

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
