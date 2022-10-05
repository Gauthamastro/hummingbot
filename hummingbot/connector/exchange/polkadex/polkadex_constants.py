# Order States
from decimal import Decimal

from hummingbot.core.api_throttler.data_types import RateLimit
from hummingbot.core.data_type.in_flight_order import OrderState

ORDER_STATE = {
    "OPEN": OrderState.OPEN,
    "CLOSED": OrderState.FILLED,
    "PARTIAL": OrderState.PARTIALLY_FILLED,
    "CANCELLED": OrderState.CANCELED,
    "REJECTED": OrderState.FAILED,
    "EXPIRED": OrderState.FAILED,
    "PENDING_CREATE": OrderState.PENDING_CREATE
}

MIN_ORDER_SIZE = Decimal(10.0)
MIN_PRICE = Decimal(0.1)
MIN_QTY = Decimal(0.1)
TRADE_EVENT_TYPE = "trade"
DIFF_EVENT_TYPE = "diff"
GRAPHQL_ENDPOINT = "https://szzsvapgkjdurfl7ijvc3vtbba.appsync-api.eu-central-1.amazonaws.com/graphql"
GRAPHQL_WSS_ENDPOINT = "https://szzsvapgkjdurfl7ijvc3vtbba.appsync-api.eu-central-1.amazonaws.com/graphql"
GRAPHQL_API_KEY = "https://szzsvapgkjdurfl7ijvc3vtbba.appsync-api.eu-central-1.amazonaws.com/graphql"

POLKADEX_SS58_PREFIX = 88

UPDATE_ORDER_STATUS_MIN_INTERVAL = 10

WS_PING_INTERVAL = 30

# Rate Limit Type
REQUEST_WEIGHT = "REQUEST_WEIGHT"
ORDERS = "ORDERS"
ORDERS_24HR = "ORDERS_24HR"

# Rate Limit time intervals
ONE_MINUTE = 60
ONE_SECOND = 1
ONE_DAY = 86400

RATE_LIMITS = [
    # Pools
    RateLimit(limit_id="polkadex", limit=1200, time_interval=ONE_MINUTE),
]
