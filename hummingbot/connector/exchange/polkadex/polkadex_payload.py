from decimal import Decimal

from hummingbot.connector.exchange.polkadex.polkadex_constants import UNIT_BALANCE
from hummingbot.core.data_type.common import OrderType, TradeType


def create_asset(asset):
    if asset == "PDEX":
        return "polkadex"
    else:
        return {"asset": int(asset)}


def create_cancel_order_req(runtime_config, order_id):
    print("order id for encoding ", order_id)
    return runtime_config.create_scale_object("H256").encode(order_id)


def create_order(runtime_config, price: Decimal, qty: Decimal, order_type, order_id: str, side, proxy, base, quote, ts):
    cid = bytearray()
    cid.extend(order_id.encode())
    cid = "0x" + bytes(cid).hex()   
    price = round(price,4)
    qty = round(qty,4)
    print("qty: ",str(qty * UNIT_BALANCE))
    print("price: ",str(price * UNIT_BALANCE))
    order = {
        "user": proxy,
        "pair": {
            "base_asset": create_asset(base),
            "quote_asset": create_asset(quote)
        },
        "qty": str(qty * UNIT_BALANCE)[0:13],#[0:8],#slicing qty
        "price": str(price * UNIT_BALANCE)[0:13], #[0:8],#slicing price
        "timestamp": ts,
        "client_order_id": cid
    }
    if order_type == OrderType.LIMIT:
        order["order_type"] = "LIMIT"
    elif order_type == OrderType.MARKET:
        order["order_type"] = "MARKET"
    else:
        print("Unsupported Order type")
        raise Exception

    if side == TradeType.BUY:
        order["side"] = "Bid"
    elif side == TradeType.SELL:
        order["side"] = "Ask"
    else:
        print("Unsupported Order side")
        raise Exception

    print(order)
    return runtime_config.create_scale_object("OrderPayloadCalledInRPC").encode(order), order
