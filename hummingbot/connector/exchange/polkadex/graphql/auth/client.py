import os
import sys
from urllib.parse import urlparse
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.appsync_auth import AppSyncApiKeyAuthentication, AppSyncJWTAuthentication
from gql import Client
from gql.transport.appsync_websockets import AppSyncWebsocketsTransport


def get_env_vars():
    url = os.environ.get("AWS_GRAPHQL_API_ENDPOINT")
    api_key = os.environ.get("AWS_GRAPHQL_API_KEY")

    if url is None or api_key is None:
        print("Missing environment variables")
        sys.exit()

    return url, api_key


# Returns a result after running graphql queries
# Doesn't take subscription commands
async def execute_query_command(query, variable_values, url,proxy_addr):
    # Extract host from url
    host = str(urlparse(url).netloc)

    auth =  AppSyncJWTAuthentication(url, proxy_addr)

    transport = AIOHTTPTransport(url=url, auth=auth)

    async with Client(transport=transport, fetch_schema_from_transport=False) as session:
        return await session.execute(query, variable_values=variable_values, parse_result=True)


# Calls the callback with the message from subscription endpoint
async def subscribe_query_command(query, variable_values, callback, host, proxy_addr):
    url, api_key = get_env_vars()
    # Extract host from url
    host = str(urlparse(url).netloc)

    auth = AppSyncJWTAuthentication(host, proxy_addr)

    transport = AppSyncWebsocketsTransport(url=url, auth=auth)

    async with Client(transport=transport, fetch_schema_from_transport=False) as session:
        async for result in session.subscribe(query, variable_values=variable_values, parse_result=True):
            callback(result)
