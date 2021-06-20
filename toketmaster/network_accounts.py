import os

from algosdk import mnemonic


class NetworkAccounts:
    """
    Creates network accounts, provisioned with algos, for test cases.
    """

    # Environment variable for path to file containing mnemonics for each test
    # account.
    _MNEMONICS_FILE_ENVVAR="MNEMONICS_FILE"

    # Indices into accounts list.
    _TOKETMASTER_IDX = 0
    _ISSUER_IDX = 1
    _FRAUDSTER_IDX = 2

    def __init__(self):
        self.accounts = self._create_accounts()

    # Create the test network account objects and return them as a list.
    def _create_accounts(self):
        mnemonics = self._read_mnemonics()
        accounts = []
        for m in mnemonics:
            # For ease of reference, adding the account mnemonic, public key, and
            # secret key, to an account dict.
            a = {}
            a["mnemonic"] = m
            a["pk"] = mnemonic.to_public_key(m)
            a["sk"] = mnemonic.to_private_key(m)
            accounts.append(a)

        return accounts

    # Read test account mnemonics from a file designated by the environment
    # variable.
    def _read_mnemonics(self):
        with open(self._get_mnemonics_fpath(), "r") as f:
            return f.readlines()

    # Get the path to the file containing the mnemonic for each test account.
    # Differs by the network being tested against.
    def _get_mnemonics_fpath(self):
        if self._MNEMONICS_FILE_ENVVAR not in os.environ:
            raise ValueError("Mnemonics filepath environment variable '{}' not set".format(
            self._MNEMONICS_FILE_ENVVAR))

        return os.environ.get(self._MNEMONICS_FILE_ENVVAR)

    def get_toketmaster_account(self):
        return self.accounts[self._TOKETMASTER_IDX]

    def get_issuer_account(self):
        return self.accounts[self._ISSUER_IDX]

    def get_fraudster_account(self):
        return self.accounts[self._FRAUDSTER_IDX]

    def get_accounts(self):
        return (self.get_toketmaster_account(), self.get_issuer_account(),
            self.get_fraudster_account())
