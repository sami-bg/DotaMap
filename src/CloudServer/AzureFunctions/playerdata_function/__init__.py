import logging

import azure.functions as func

"""
Player-data Function - Stores player data in redis, responds to clients asking for player-data 
"""


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
