"""

Heroes:

Masks the minimap pixels against a fully dark minimap with no buildings except the ancients. Each centroid that is not
part of the default minimap gets classified as one of the 9 other players via color detection.

    Player heroes:
        Player's hero is detected via game-state integration.
    Other heroes:
        If a centroid is classified with multiple player colors, then we conclude the players are on top of each other
        and give the coordinates of each player as the center of the centroid + some radius r away from the middle as
        to be able to display multiple circles on top of each other on the coordinates returned.

Towers & structures:

Friendly structures are detected via game-state integration.

Enemy structures are detected via checking for their presence on hardcoded coordinates - hardcoded coordinates exist for
both friendly and enemy teams.

Outposts:

Outposts are in the same position every time. Their parity is decided via color detection.

Couriers, illusion units, creeps, summoned units, map drawings, map pings:

TBD.

 For illusions, maybe just send coordinates and magnitude? That way PL illusion stack is just a bigger colored icon.

Wards:

TBD.

"""