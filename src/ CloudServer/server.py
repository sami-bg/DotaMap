import json
from aiohttp import web
import redis

with open("../cloud_settings.json") as endpointConfig:
    endpointStringsObject = json.load(endpointConfig)
    endpointConfig.close()

BUILDINGS_GET_ENDPOINT = endpointStringsObject['buildings_get_endpoint']
BUILDINGS_POST_ENDPOINT = endpointStringsObject['buildings_post_endpoint']
PLAYERS_GET_ENDPOINT = endpointStringsObject['players_get_endpoint']
PLAYERS_POST_ENDPOINT = endpointStringsObject['players_post_endpoint']

# Use the requirepass option in order to add an additional layer of security so that clients will require to
# authenticate using the AUTH command. Use spiped or another SSL tunneling software in order to encrypt traffic
# between Redis servers and Redis clients if your environment requires encryption.

r = redis.Redis(host='127.0.0.1',
                port=6379, db=0)
# Start Cloud server
routes = web.RouteTableDef()


# TODO : This file would start redis locally, receives data from streamer, sends data to viewers.
#  This has to be done on a linux environment for redis (hence, remote server, among other reasons)
#  How the hell do I test it then? strange times. Let's see.
# Dispenses coordinates to viewer
@routes.get(f'/{PLAYERS_GET_ENDPOINT}')
async def send_player_data(request: web.Request) -> web.Response:
    args = await request.json()
    # Add the user
    # ...
    return web.Response(text=f"JSON Received.")


# Receive coordinates from streamer
@routes.post(f'/{[PLAYERS_POST_ENDPOINT]}')
async def send_player_data(request: web.Request) -> web.Response:
    args = await request.json()
    # Add the user
    # ...
    return web.Response(text=f"JSON Received.")


# Dispense coordinates from streamer
@routes.get(f'/{BUILDINGS_GET_ENDPOINT}')
async def send_building_data(request: web.Request) -> web.Response:
    args = await request.json()
    # Get local_timestamp & stream_timestamp
    # Query from redis timeseries
    # Add the user
    # ...
    return web.Response(text=f"JSON Buildings Received.")


# Receive coordinates from streamer
@routes.get(f'/{BUILDINGS_POST_ENDPOINT}')
async def init_app() -> web.Application:
    gsi = web.Application()
    gsi.add_routes(routes)
    # TODO: Init redis with redisJSON
    redis_ping = r.ping()
    print("Ping returned : " + str(redis_ping))
    return gsi


print(r.ping())
# web.run_app(init_app(), port=6000)
