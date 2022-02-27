import logging

import azure.functions as func

"""
Player-data Function - Stores player data in redis, responds to clients asking for player-data 
"""

# TODO - This should both use WebSockets (Twitch client connection) and HTTP/TCP (Streamer server connection)
# How does WebSockets work when each twitch client needs separate information? Maybe it still does?
# Should I make my own protocol?

# I suspect TCP is enough. Problems arise when most viewers have little delay to streamer, as request frequency
# is inversely proportional to delay (1s behind = 1 request per second, 5s behind = 1 request per 5 seconds).

# What about BOTH? Temporally close twitch clients subscribe to websocket solution, temporally far stick to web requests

# But this is over-engineering, for now...


def process_incoming_player_data():
    pass


def dispense_outgoing_player_data():
    pass


def main(request: func.HttpRequest):
    logging.info(f'Request Method: {request.method}')

    if request.method == 'GET':
        return func.HttpResponse("Received GET")

    # POST
    try:
        match_id = request.get_json()['match_id']
    except (ValueError, KeyError):
        return func.HttpResponse(f"Incorrect JSON: {request}")

    return func.HttpResponse(f'Connected - Match ID: {match_id}')
