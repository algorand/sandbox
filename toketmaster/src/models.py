from algosdk import account


class Wallet:
    def __init__(self):
        sk, pk = account.generate_account()
        self.secret_key = sk
        self.public_key = pk
