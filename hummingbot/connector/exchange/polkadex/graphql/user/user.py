import json

from gql import gql
from gql.transport.exceptions import TransportQueryError

from hummingbot.connector.exchange.polkadex.graphql.auth.client import execute_query_command

async def cancel_order(params, url, api_key):
    mutation = gql(
        """
    mutation CancelOrder($input: UserActionInput!) {
        cancel_order(input: $input)
    }
        """
    )
    print("params: ", params)
    encoded_params = json.dumps({"CancelOrder": params});
    variables = {"input": {"payload": encoded_params}}
    try:
        result = await execute_query_command(mutation, variables, url, api_key)
        print("Cancel order result: ", result)
        return result["cancel_order"]
    except TransportQueryError as executionErr:
        print("Error while cancelling orders: ", executionErr.errors)
        raise Exception("TransportQueryError")


async def place_order(params, url, api_key):
    print("Inside graphQl place order")
    try:
        mutation = gql(
            """
        mutation PlaceOrder($input: UserActionInput!) {
            place_order(input: $input)
        }
            """
        )
        encoded_params = json.dumps({"PlaceOrder": params})

        variables = {"input": {"payload": encoded_params}}
        
        print("execute_query_command called")
        result = await execute_query_command(mutation, variables, url, api_key)
        print("Place order result: ", result)
        return result["place_order"]
    except:
        print("---place_order in user folder passing an exception---")



#working as expected
async def get_all_balances_by_main_account(main, endpoint, api_key):
    query = gql(
        """
query getAllBalancesByMainAccount($main: String!) {
  getAllBalancesByMainAccount(main_account: $main) {
    items {
      a
      f
      r
    }
  }
}
""")
    variables = {"main": main}

    result = await execute_query_command(query, variables, endpoint, api_key)
    return result["getAllBalancesByMainAccount"]["items"]



async def find_order_by_main_account(main, order_id, market, endpoint, api_key):
    # TODO: Should We change this to client order id???
    query = gql(
        """
query findOrderByMainAccount($main: String!, $market: String!, $order_id: String!) {
  findOrderByMainAccount(main_account: $main, market: $market, order_id: $order_id) {
    afp
    cid
    fee
    fq
    id
    m
    ot
    p
    q
    s
    st
    t
    u
  }
}
""")
    variables = {"order_id": order_id, "market": market, "main": main}
    result = await execute_query_command(query, variables, endpoint, api_key)
    return result["findOrderByMainAccount"]

async def get_main_acc_from_proxy_acc(proxy, endpoint, api_key):
    query = gql(
        """
query findUserByProxyAccount($proxy_account: String!) {
  findUserByProxyAccount(proxy_account: $proxy_account) {
    items
  }
}
""")
    variables = {"proxy_account": proxy}

    result = await execute_query_command(query, variables, endpoint, api_key)
    main = result["findUserByProxyAccount"]["items"][0].split(",")[2][11:-1]
    print("FindUser by proxy result: ", main)
    # TODO: Handle error if main account not found
    return main


# async def get_asset_balance_by_main_account(main, asset):
#     query = gql(
#         """
# query findBalanceByMainAccount($asset: String!, $main: String!) {
#   findBalanceByMainAccount(
#     asset: $asset,
#     main_account: $main) {
#     free
#     pending_withdrawal
#     reserved
#   }
# }
# """)
#     variables = {"asset": asset, "main": main}

#     result = await execute_query_command(query, variables)
#     return result["findBalanceByMainAccount"]


# async def list_open_orders_by_main_account(main, nextToken, limit):
#     query = gql(
#         """
# query listOpenOrdersByMainAccount($main: String!, $nextToken: String, $limit: Int) {
#   listOpenOrdersByMainAccount(
#     main_account: $main,
#     nextToken: $nextToken,
#     limit: $limit) {
#     items {
#       avg_filled_price
#       fee
#       filled_quantity
#       id
#       m
#       order_type
#       price
#       qty
#       side
#       status
#       time
#     }
#     nextToken
#   }
# }
# """)
#     variables = {"main": main}

#     if limit is not None:
#         variables["limit"] = limit
#     if nextToken is not None:
#         variables["nextToken"] = nextToken

#     result = await execute_query_command(query, variables)
#     return result["listOpenOrdersByMainAccount"]



# async def list_order_history_by_main_account(main, from_date, to_date, nextToken, limit):
#     query = gql(
#         """
# query listOrderHistorybyMainAccount($from: AWSDateTime!, $to: AWSDateTime!, $main: String!, $nextToken: String, $limit: Int) {
#   listOrderHistorybyMainAccount(
#     from: $from,
#     main_account: $main,
#     to: $to,
#     nextToken: $nextToken,
#     limit: $limit) {
#     items {
#       avg_filled_price
#       fee
#       filled_quantity
#       id
#       order_type
#       price
#       qty
#       side
#       status
#       time
#     }
#     nextToken
#   }
# }
# """)
#     variables = {"from": from_date.isoformat(timespec="seconds") + "Z",
#                  "to": to_date.isoformat(timespec="seconds") + "Z", "main": main}

#     if limit is not None:
#         variables["limit"] = limit
#     if nextToken is not None:
#         variables["nextToken"] = nextToken

#     result = await execute_query_command(query, variables)
    # return result["listOrderHistorybyMainAccount"]

# async def find_user_by_main_account(main):
#     query = gql(
#         """
# query findUserByMainAccount($main: String!) {
#   findUserByMainAccount(main_account: $main) {
#     proxy_accounts
#   }
# }
# """)
#     variables = {"main": main}

#     result = await execute_query_command(query, variables)
#     return result["findUserByMainAccount"]


# async def list_trades_by_main_account(main, from_date, to_date, nextToken, limit):
#     query = gql(
#         """
# query listTradesByMainAccount($from: AWSDateTime!, $to: AWSDateTime!, $main: String!, $nextToken: String, $limit: Int) {
#   listTradesByMainAccount(
#     from: $from,
#     main_account: $main,
#     to: $to,
#     nextToken: $nextToken,
#     limit: $limit) {
#   nextToken
#     items {
#       m
#       p
#       q
#       s
#       time
#     }
#   }
# }
# """)
#     variables = {"from": from_date.isoformat(timespec="seconds") + "Z",
#                  "to": to_date.isoformat(timespec="seconds") + "Z", "main": main}

#     if limit is not None:
#         variables["limit"] = limit
#     if nextToken is not None:
#         variables["nextToken"] = nextToken

#     result = await execute_query_command(query, variables)
#     return result["listTradesByMainAccount"]


# async def list_transaction_by_main_account(main, from_date, to_date, nextToken, limit):
#     query = gql(
#         """
# query listTransactionsByMainAccount($from: AWSDateTime!, $to: AWSDateTime!, $main: String!, $nextToken: String, $limit: Int) {
#   listTransactionsByMainAccount(
#     from: $from,
#     main_account: $main,
#     to: $to,
#     nextToken: $nextToken,
#     limit: $limit) {
#     nextToken
#     items {
#       amount
#       asset
#       fee
#       status
#       time
#       txn_type
#     }
#   }
# }
# """)
#     variables = {"from": from_date.isoformat(timespec="seconds") + "Z",
#                  "to": to_date.isoformat(timespec="seconds") + "Z", "main": main}

#     if limit is not None:
#         variables["limit"] = limit
#     if nextToken is not None:
#         variables["nextToken"] = nextToken

#     result = await execute_query_command(query, variables)
    # return result["listTransactionsByMainAccount"]
