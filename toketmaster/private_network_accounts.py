from algosdk import mnemonic


class PrivateNetworkAccounts:
    """
    TODO(hv): Doc
    """

    _TOKETMASTER_IDX = 0
    _ISSUER_IDX = 1
    _FRAUDSTER_IDX = 2

    def __init__(self):
        self._mnemonics = self._read_mnemonics()
        self.accounts = self._create_accounts()

    def _read_mnemonics(self):
        with open("/tmp/mnemonics.txt", "r") as f:
            return f.readlines()

    def _create_accounts(self):
        # For ease of reference, adding the account public and private keys to an
        # accounts dict.
        accounts = []
        for m in self._mnemonics:
            a = {}
            a["pk"] = mnemonic.to_public_key(m)
            a["sk"] = mnemonic.to_private_key(m)
            accounts.append(a)

        return accounts

    def get_toketmaster_account(self):
        return self.accounts[self._TOKETMASTER_IDX]

    def get_issuer_account(self):
        return self.accounts[self._ISSUER_IDX]

    def get_fraudster_account(self):
        return self.accounts[self._FRAUDSTER_IDX]

    def get_accounts(self):
        return (self.get_toketmaster_account(), self.get_issuer_account(),
            self.get_fraudster_account())
