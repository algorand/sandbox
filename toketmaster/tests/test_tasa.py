import time
import unittest

from algosdk.error import IndexerHTTPError

from toketmaster.src import client, models, tasa


def wait_to_complete(func, *args, **kwargs):
    while True:
        try:
            return func(*args, **kwargs)

        except IndexerHTTPError:
            time.sleep(1)


class TestTasaIsCreated(unittest.TestCase):
    def setUp(self) -> None:
        self.toketmaster_wallet = models.Wallet(
            public_key='PGFSRHMDZ2FM7GGTIAXU7BGPJENEARFCU2SYE2DLD44EIU2Z6VPF7AQEPQ',
            secret_key='KONd7E3fz4p6ar2FzYDivkcBhDeEQKq/qtCIty9+trR5iyidg86Kz5jTQC9PhM9JGkBEoqalgmhrHzhEU1n1Xg=='
        )

    def test_tasa_is_created(self):
        tasa_creation_id = tasa.create_tasa(creator=self.toketmaster_wallet,
                                            manager=self.toketmaster_wallet,
                                            freeze=self.toketmaster_wallet,
                                            reserve=self.toketmaster_wallet,
                                            clawback=self.toketmaster_wallet,
                                            fee=5,
                                            unit_name="TASA",
                                            asset_name="Domvanin",
                                            url="domvanin.org")

        # transaction doesn't post immediately
        r = wait_to_complete(func=client.indexer_client.transaction, txid=tasa_creation_id)
        tx_params = r['transaction']['asset-config-transaction']['params']

        assert tx_params['creator'] == self.toketmaster_wallet.public_key
        assert tx_params['manager'] == self.toketmaster_wallet.public_key
        assert tx_params['clawback'] == self.toketmaster_wallet.public_key
        assert tx_params['reserve'] == self.toketmaster_wallet.public_key
        assert tx_params['freeze'] == self.toketmaster_wallet.public_key
        assert tx_params['total'] == 1
        assert tx_params['unit-name'] == 'TASA'
        assert tx_params['name'] == 'Domvanin'
        assert tx_params['url'] == 'domvanin.org'


class TestTasaIsTransferred(unittest.TestCase):
    def setUp(self) -> None:
        self.toketmaster_wallet = models.Wallet(
            public_key='PGFSRHMDZ2FM7GGTIAXU7BGPJENEARFCU2SYE2DLD44EIU2Z6VPF7AQEPQ',
            secret_key='KONd7E3fz4p6ar2FzYDivkcBhDeEQKq/qtCIty9+trR5iyidg86Kz5jTQC9PhM9JGkBEoqalgmhrHzhEU1n1Xg=='
        )

        self.client_wallet = models.Wallet(
            public_key='CVFHOVYERCILMXWUBJZKMINGFF5OJ5A5QDMVXSDZL2L5DEIVZCKLP2XIBI',
            secret_key='Z0vn6E6/j/vWqpG8+0MqVXWtDLdtB1tILF46SpcSr1oVSndXBIiQtl7UCnKmIaYpeuT0HYDZW8h5XpfRkRXIlA=='
        )
        _tasa_creation_id = tasa.create_tasa(creator=self.toketmaster_wallet,
                                             manager=self.toketmaster_wallet,
                                             freeze=self.toketmaster_wallet,
                                             reserve=self.toketmaster_wallet,
                                             clawback=self.toketmaster_wallet,
                                             fee=5,
                                             unit_name="TASA",
                                             asset_name="Domvanin",
                                             url="domvanin.org")
        self.tasa_id = wait_to_complete(func=tasa.get_tasa_id, tasa_create_txid=_tasa_creation_id)

    def test_tasa_is_transferred(self):
        transfer_id = tasa.transfer_tasa(
            from_=self.toketmaster_wallet,
            to=self.client_wallet,
            tasa_id=self.tasa_id,
            fee=8)

        r = wait_to_complete(func=client.indexer_client.transaction, txid=transfer_id)
        tx_params = r['transaction']['asset-transfer-transaction']

        assert tx_params['amount'] == 1
        assert tx_params['asset-id'] == self.tasa_id
        assert tx_params['receiver'] == self.client_wallet.public_key

