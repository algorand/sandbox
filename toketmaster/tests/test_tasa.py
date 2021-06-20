import time
import unittest

from algosdk.error import IndexerHTTPError

from toketmaster.src import client, models, tasa


class TestTasa(unittest.TestCase):
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
        while True:
            try:
                r = client.indexer_client.transaction(txid=tasa_creation_id)
                break

            except IndexerHTTPError:
                time.sleep(1)

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

