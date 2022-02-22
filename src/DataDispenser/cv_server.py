"""

Combines all the other modules to send data to the server that the client Twitch extension will interface with:

    All 10 hero coordinates.
    Tower status updates.
    Outpost status updates.
    Structure status updates.
    Game state changes.

First, reads the game state to check if a game has started.
Once a game has started (not just draft), reads one frame to get minimap coordinates.
It takes each frame from OBS after that and detects unit/structure coordinates.
It sends coordinates to the remote server.

Then, the remote server stores them on Redis for a particular streamer.

"""