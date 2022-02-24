import json
from aiohttp import web

with open("../cloud_settings.json") as endpointConfig:
    endpointStringsObject = json.load(endpointConfig)
    endpointConfig.close()

BUILDINGS_ENDPOINT = endpointStringsObject['buildings_endpoint']
PLAYERS_ENDPOINT = endpointStringsObject['players_endpoint']

# Start Cloud server
routes = web.RouteTableDef()


# TODO : This file would start redis locally, receives data from streamer, sends data to viewers
@routes.get(f'/{PLAYERS_ENDPOINT}')
async def send_player_data(request: web.Request) -> web.Response:
    args = await request.json()
    # Add the user
    # ...
    return web.Response(text=f"JSON Received.")


@routes.get(f'/{BUILDINGS_ENDPOINT}')
async def send_building_data(request: web.Request) -> web.Response:
    args = await request.json()
    # Get local_timestamp & stream_timestamp
    # Query from redis timeseries
    # Add the user
    # ...
    return web.Response(text=f"JSON Buildings Received.")


async def init_app() -> web.Application:
    gsi = web.Application()
    gsi.add_routes(routes)
    # TODO: Init redis with redisJSON
    redis_ping = r.ping()
    print("Ping returned : " + str(redis_ping))
    return gsi


web.run_app(init_app(), port=6000)
