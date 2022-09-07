from unittest import TestCase

from hummingbot.connector.exchange.polkadex.polkadex_utils import convert_asset_to_ticker, convert_pair_to_market, convert_ticker_to_enclave_trading_pair

class PolkadexUtilsUnitTests(TestCase):
    def test_convert_asset_to_ticker(self):
        convert_asset_to_ticker("polkdex")
        convert_asset_to_ticker({"asset":1})

    def test_convert_pair_to_market(self):
        convert_pair_to_market({
            "base_asset": "polkadex",
            "quote_asset": "polkadex"
        })
    
    def test_convert_pair_to_market_asset(self):
        convert_pair_to_market({
            "base_asset": {"asset": "1"},
            "quote_asset": {"asset": "1"}
        })

    def test_convert_ticker_to_enclave_trading_pair(self):
        convert_ticker_to_enclave_trading_pair(market="PDEX-1")