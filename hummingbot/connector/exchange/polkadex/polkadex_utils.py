from decimal import Decimal

from hummingbot.client.config.config_methods import using_exchange
from hummingbot.client.config.config_var import ConfigVar
from hummingbot.connector.exchange.polkadex.polkadex_payload import create_asset
from hummingbot.core.data_type.trade_fee import TradeFeeSchema
from hummingbot.connector.exchange.polkadex import polkadex_constants as CONSTANTS


CENTRALIZED = True
EXAMPLE_PAIR = "PDEX-1"

DEFAULT_FEES = TradeFeeSchema(
    maker_percent_fee_decimal=Decimal("0.002"),
    taker_percent_fee_decimal=Decimal("0.002"),
    buy_percent_fee_deducted_from_returns=True
)

KEYS = {
    "polkadex_seed_phrase":
        ConfigVar(key="polkadex_seed_phrase",
                  prompt="Enter polkadex_seed_phrase>>> ",
                  required_if=using_exchange("polkadex"),
                  is_secure=True,
                  is_connect_key=True),
}


def convert_asset_to_ticker(asset):
    if "asset" in asset:
        return asset["asset"]
    elif "polkadex" in asset:
        return "PDEX"


def convert_pair_to_market(pair):
    base = str(pair["base_asset"])
    quote = str(pair["quote_asset"])
    return base + "-" + quote, base, quote


def convert_ticker_to_enclave_trading_pair(market):
    pair = {
        "base_asset": create_asset(market.split("-")[0]),
        "quote_asset": create_asset(market.split("-")[1])
    }
    return pair

def parse_price_or_qty(value):
    print("var type: ",type(value))
    print("value: ",value)
    return Decimal(value)
