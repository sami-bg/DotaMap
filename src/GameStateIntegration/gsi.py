import subprocess
from aiohttp import web
from src.Models.location import Location
import dota2gsi
import json
import redis

"""
Combines all the other modules to send data to the server that the client Twitch extension will interface with:

    All 10 hero coordinates.
    Tower status updates.
    Outpost status updates.
    Structure status updates.
    Game state changes.
 
It starts the node GSI server via a non-blocking subprocess call, then repeatedly polls GSI Server for:

    Game started/ended.
    Heroes alive/dead.
    Friendly structure HPs.

    Detecting player's:
        Position
        Team parity
        Player numbers and colors
        Heroes in match
        Fortification cooldown (?)


Uses https://github.com/xzion/dota2-gsi.

First, reads the game state to check if a game has started. This is done via a node GSI server that is run as a
non-blocking subprocess.

Once a game has started (not just draft), reads one frame to get minimap coordinates.
It takes each frame from OBS after that and detects unit/structure coordinates.
It sends coordinates to the remote server.

Then, the remote server stores them on Redis for a particular streamer.

IMPORTANT: https://github.com/xzion/dota2-gsi#configuring-the-dota-2-client
'To configure the Dota client to report gamestate, you need to add a config file in
steamapps\common\dota 2 beta\game\dota\cfg\gamestate_integration\.

The file must use the name pattern called gamestate_integration_*.cfg, for example gamestate_integration_dota2-gsi.cfg.'
"""

with open("../app.json") as redisConfig:
    redisJsonObject = json.load(redisConfig)
    redisConfig.close()

REDIS_HOST_NAME = redisJsonObject['redis']['host_name']
REDIS_ACCESS_KEY = redisJsonObject['redis']['primary_access_key']
REDIS_CONNECTION_STRING = redisJsonObject['redis']['primary_connection_string']
REDIS_SSL_PORT = redisJsonObject['redis']['ssl_port']

r = redis.StrictRedis(host=REDIS_HOST_NAME, port=REDIS_SSL_PORT,
                      password=REDIS_ACCESS_KEY, ssl=True)


def start_node_gsi_server():
    # Popen is non-blocking.
    subprocess.Popen(['node', '.\\gsi_server.js'])
    return


# Start GSI server
routes = web.RouteTableDef()
game_started = False
player_coordinates: Location = Location(0, 0)


# Defines server for which events triggered in node GSI server will send notifications to
def process_gsi(args):
    print(json.loads(args['body']))




def send_to_redis(data):
    # matchid_[all/radiant/dire]_player_[0-9] , value: (x, y, hero_id)
    # matchid_[all/radiant/dire]_building_[...] , value : alive/dead
    pass


@routes.post('/json')
async def receive_gsi(request: web.Request) -> web.Response:
    args = await request.json()
    # Add the user
    # ...
    process_gsi(args)
    return web.Response(text=f"JSON Received.")


async def init_app() -> web.Application:
    gsi = web.Application()
    gsi.add_routes(routes)
    redis_ping = r.ping()
    print("Ping returned : " + str(redis_ping))
    # start_node_gsi_server()
    return gsi


# NOTE: top-right xpos y-pos:
# Hero y position: 6688
# Hero x position: 7136
# Most negative x pos: -7648
# Most negative y pos: -7207
# Most positive y: 6906
# Most positive x: 7456
# 0,0 is the middle of the map, about dire mid stairs. top left is -x +y, top right is +x+y, bottom left is -x-y, etc.
web.run_app(init_app(), port=8080)
