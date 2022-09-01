import asyncio
import json 
import re 
import unittest
from typing import Awaitable 
from unittest.mock import AsyncMock, MagicMock, patch 
from decimal import Decimal

from aioresponses.core import aioresponses 
from bidict import bidict

from hummingbot.connector.test_support.network_mocking_assistant import NetworkMockingAssistant
from hummingbot.core.data_type.order_book import OrderBook
from hummingbot.core.data_type.order_book_message import OrderBookMessage 
from hummingbot.core.data_type.common import OrderType, TradeType
from hummingbot.core.data_type.in_flight_order import InFlightOrder, OrderState, OrderUpdate, TradeUpdate

# Polkadex Classes 
from hummingbot.connector.exchange.polkadex.polkadex_exchange import PolkadexExchange 
from hummingbot.connector.exchange.polkadex.polkadex_order_book_data_source import PolkadexOrderbookDataSource

class PolkadexExchangeUnitTests(unittest.TestCase):
    level = 0 

    @classmethod
    def setUpClass(cls) -> None: 
        super().setUpClass()
        cls.ev_loop = asyncio.get_event_loop()
        cls.base_asset = "COINALPHA"
        cls.quote_asset = "HBOT"
        cls.trading_pair = f"{cls.base_asset}-{cls.quote_asset}"
        cls.ex_trading_pair = cls.base_asset + cls.quote_asset
        cls.domain = "com"

    def setUp(self) -> None:
        super().setUp()
        self.log_records = [] 
        self.listening_task = None 
        self.mocking_assistant = NetworkMockingAssistant
        self.resume_test_event = asyncio.Event()
        # Polkadex Connector 
        self.connector = PolkadexExchange(
                polkadex_seed_phrase = "empower open normal dream vendor day catch flee entry monitor like april"
        )
        # Polkadex OrderBookDataSource 
        self.data_source = PolkadexOrderbookDataSource(
                trading_pairs=[], 
                connector = self.connector, 
                api_factory = self.connector._web_assistants_factory,
                api_key = " ")
        
        self.data_source.logger().setLevel(1)
        self.data_source.logger().addHandler(self)


    def tearDown(self) -> None:
        self.listening_task and self.listening_task.cancel()
        super().tearDown()

    def handle(self, record):
        self.log_records.append(record)

    def _is_logged(self, log_level: str, message: str) -> bool:
        return any(record.levelname == log_level and record.getMessage() == message
                   for record in self.log_records)

    def _create_exception_and_unlock_test_with_event(self, exception):
        self.resume_test_event.set()
        raise exception

    def async_run_with_timeout(self, coroutine: Awaitable, timeout: float = 1):
        ret = self.ev_loop.run_until_complete(asyncio.wait_for(coroutine, timeout))
        return ret


    @aioresponses()
    def test_get_last_traded_price(self, mock_api):
        raw_url = "https://2cv3skldsvh3fjsgsuftnxzo5a.appsync-api.ap-south-1.amazonaws.com/graphql"
        resp = {
            "data": {
                "getRecentTrades": {
                    "items": [{
                        "p": 20
                    }]
                }
            }
        }
        mock_api.post(raw_url, body=json.dumps(resp))
        order_book_message: float = self.async_run_with_timeout(
                self.connector._get_last_traded_price(self.trading_pair)
        )

        self.assertEqual(20.0, order_book_message)

    # Need response from `get_all_markets`
    @aioresponses()
    def test_initialize_trading_pair_symbols(self, mock_api):
        raw_url = "https://2cv3skldsvh3fjsgsuftnxzo5a.appsync-api.ap-south-1.amazonaws.com/graphql"
        resp = {
  "data": {
    "getAllMarkets": {
      "items": [
        {
          "market": "PDEX-1",
          "max_trade_amount": "1000000000000000",
          "min_qty": "1000000000000",
          "min_trade_amount": "1000000000000"
        }
      ]
    }
  }
}
        mock_api.post(raw_url, body=json.dumps(resp))
        order_book_message = self.async_run_with_timeout(
                self.connector._initialize_trading_pair_symbol_map()
        )
    
    # Need query from user.py in graphql
    @aioresponses()
    def test_update_balances(self, mock_api):
        raw_url = "https://2cv3skldsvh3fjsgsuftnxzo5a.appsync-api.ap-south-1.amazonaws.com/graphql"
        resp = {
            "data": {
                "findUserByProxyAccount": {
                    "items": [
                        "{eid=1, hash_key=proxy-esqacydQWhJ9D7Wg5G7VZfPYGd6uM6X7kk8Jq3fyNDh2HvYrk, range_key=esoGSWG1uQFx1HPLpdZgsNRZBdtPLtpkSUruL1ZFqjLH3e9B4}"
                    ]
                }
            }
        }
        mock_api.post(raw_url, body=json.dumps(resp))
        resp = {
  "data": {
    "getAllBalancesByMainAccount": {
      "items": [
        {
          "a": "1",
          "f": "94000000000000",
          "p": "0",
          "r": "6000000000000"
        },
        {
          "a": "PDEX",
          "f": "99000000000000",
          "p": "0",
          "r": "1000000000000"
        }
      ]
    }
  }
}
        mock_api.post(raw_url, body=json.dumps(resp))
        order_book_message = self.async_run_with_timeout(
                self.connector._update_balances()
        )
    
    # Need to query user.py in graphql
    @aioresponses()
    def test_update_order_status(self, mock_api):
        raw_url = "https://2cv3skldsvh3fjsgsuftnxzo5a.appsync-api.ap-south-1.amazonaws.com/graphql"
        resp = {
            "data": {
                "findUserByProxyAccount": {
                    "items": [
                        "{eid=1, hash_key=proxy-esqacydQWhJ9D7Wg5G7VZfPYGd6uM6X7kk8Jq3fyNDh2HvYrk, range_key=esoGSWG1uQFx1HPLpdZgsNRZBdtPLtpkSUruL1ZFqjLH3e9B4}"
                    ]
                }
            }
        }
        mock_api.post(raw_url, body=json.dumps(resp))
        order_book_message = self.async_run_with_timeout(
                self.connector._update_order_status()
        )

    @aioresponses()
    def test_cancel_order(self, mock_api):
        order = InFlightOrder(
            client_order_id="123",
            trading_pair=self.trading_pair,
            order_type=OrderType.LIMIT,
            trade_type=TradeType.BUY,
            amount=Decimal("1000.0"),
            creation_timestamp=1640001112.0,
            price=Decimal("1.0"),
        )

        order_book_message = self.async_run_with_timeout(
            self.connector._place_cancel(order_id="123", tracked_order=order)
        )
        self.assertEqual(order_book_message,False)

    @aioresponses()
    def test_place_order(self, mock_api):
        order = InFlightOrder(
            client_order_id="123",
            trading_pair=self.trading_pair,
            order_type=OrderType.LIMIT,
            trade_type=TradeType.BUY,
            amount=Decimal("1000.0"),
            creation_timestamp=1640001112.0,
            price=Decimal("1.0"),
        )

        
        order_book_message = self.async_run_with_timeout(
            self.connector._place_order(order_id="123", trading_pair=self.trading_pair, amount=Decimal("1000.0"), trade_type=TradeType.BUY, order_type=OrderType.LIMIT, price=Decimal("1000.0"))
        )

        



        


