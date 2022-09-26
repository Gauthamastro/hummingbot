from decimal import Decimal
from venv import create

from hummingbot.core.data_type.common import OrderType, TradeType


def create_asset(asset):
    if asset == "PDEX":
        return "polkadex"
    else:
        return {"asset": int(asset)}


def create_cancel_order_req(runtime_config, order_id):
    print("order id for encoding ", order_id)
    return runtime_config.create_scale_object("H256").encode(order_id)

''' pub client_order_id: ClientOrderId,
    pub user: AccountId,
    pub main_account: AccountId,
    pub pair: String,
    pub side: OrderSide,
    pub order_type: OrderType,
    pub quote_order_quantity: String,
    // Quantity is defined in base asset
    pub qty: String,
    // Price is defined in quote asset per unit base asset
    pub price: String,
    pub timestamp: i64,
'''

def create_order(runtime_config, price: Decimal, qty: Decimal, order_type, order_id: str, side, proxy,main, base, quote, ts):
    cid = bytearray()
    cid.extend(order_id.encode())
    cid = "0x" + bytes(cid).hex()   
    price = round(price,4)
    qty = round(qty,4)
    print("qty: ",str(qty))
    print("price: ",str(price))
    order = {
        "user": proxy,
        "main_account":  main,
        "pair": str(base)+"-"+str(quote),
        "qty": str(qty)[0:12],#[0:8],#ToDo: May fail
        "price": str(price)[0:12], #[0:8],#ToDo: May fail
        "quote_order_quantity": "0",
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
    return runtime_config.create_scale_object("OrderPayload").encode(order), order
