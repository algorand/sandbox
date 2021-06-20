import os

from algosdk import mnemonic


class NetworkAccounts:
    """
    TODO(hv): Doc
    """

    _MNEMONICS_FILE_ENVVAR="MNEMONICS_FILE"

    _TOKETMASTER_IDX = 0
    _ISSUER_IDX = 1
    _FRAUDSTER_IDX = 2

    def __init__(self):
        self.accounts = self._create_accounts()

    def _create_accounts(self):
        mnemonics = self._read_mnemonics()
        # For ease of reference, adding the account public and private keys to an
        # accounts dict.
        accounts = []
        for m in mnemonics:
            a = {}
            a["pk"] = mnemonic.to_public_key(m)
            a["sk"] = mnemonic.to_private_key(m)
            accounts.append(a)

        return accounts

    def _read_mnemonics(self):
        with open(self._get_mnemonics_fpath(), "r") as f:
            return f.readlines()

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
