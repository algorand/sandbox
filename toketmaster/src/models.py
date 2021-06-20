from algosdk import account


class Wallet:
    def __init__(self, public_key: str, secret_key: str):
        self.public_key = public_key
        self.secret_key = secret_key

    @classmethod
    def create_new(cls):
        sk, pk = account.generate_account()
        return cls(public_key=pk, secret_key=sk)
