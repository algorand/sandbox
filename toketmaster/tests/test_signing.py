import unittest

import pytest
from nacl.exceptions import BadSignatureError

from toketmaster.src import models, message


class TestSignature(unittest.TestCase):
    def setUp(self) -> None:
        self.client_wallet = models.Wallet(
            public_key='CVFHOVYERCILMXWUBJZKMINGFF5OJ5A5QDMVXSDZL2L5DEIVZCKLP2XIBI',
            secret_key='Z0vn6E6/j/vWqpG8+0MqVXWtDLdtB1tILF46SpcSr1oVSndXBIiQtl7UCnKmIaYpeuT0HYDZW8h5XpfRkRXIlA=='
        )
        self.attacker_wallet = models.Wallet.create_new()
        self.message = message.create_message(tasa_id='17084345')

    def test_proper_signature_works(self):
        signature = message.sign_message(message=self.message, secret_key=self.client_wallet.secret_key)

        signature_is_legit = message.verify_message(
            message=self.message,
            public_key=self.client_wallet.public_key,
            signature=signature)

        assert signature_is_legit

    def test_forged_signature_fails(self):
        signature = message.sign_message(message=self.message, secret_key=self.attacker_wallet.secret_key)

        with pytest.raises(BadSignatureError):
            _ = message.verify_message(
                message=self.message,
                public_key=self.client_wallet.public_key,
                signature=signature
            )
