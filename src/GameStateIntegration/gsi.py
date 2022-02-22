import subprocess
from aiohttp import web
from src.Models.location import Location

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
"""


def start_node_gsi_server():
    # Popen is non-blocking.
    subprocess.Popen(['node', '.\\gsi_server.js'])
    return


# Start GSI server
routes = web.RouteTableDef()
game_started = False
player_coordinates: Location = Location(0, 0)
start_node_gsi_server()


# Defines server for which events triggered in node GSI server will send notifications to
def process_gsi(args):
    pass


@routes.post('/json')
# ?page=1&uppercase=true
async def receive_gsi(request: web.Request) -> web.Response:
    args = await request.json()
    # Add the user
    # ...
    process_gsi(args)
    return web.Response(text="JSON Received.")


async def init_app() -> web.Application:
    gsi = web.Application()
    gsi.add_routes(routes)
    return gsi


web.run_app(init_app())


