var d2gsi = require("dota2-gsi");
var server = new d2gsi();
const axios = require("axios").default;

var global_gsi = {
  team: "",
  building: null, // I'd rather just slap the entire building json here tbh
  players: {
    player0: {
      xpos: -1,
      ypos: -1,
      name: "",
      heroId: -1,
    },
    player1: {
      xpos: -1,
      ypos: -1,
      name: "",
      heroId: -1,
    },
    player2: {
      xpos: -1,
      ypos: -1,
      name: "",
      heroId: -1,
    },
    player3: {
      xpos: -1,
      ypos: -1,
      name: "",
      heroId: -1,
    },
    player4: {
      xpos: -1,
      ypos: -1,
      name: "",
      heroId: -1,
    },
    // Dire:
    player5: {
      xpos: -1,
      ypos: -1,
      name: "",
      heroId: -1,
    },
    player6: {
      xpos: -1,
      ypos: -1,
      name: "",
      heroId: -1,
    },
    player7: {
      xpos: -1,
      ypos: -1,
      name: "",
      heroId: -1,
    },
    player8: {
      xpos: -1,
      ypos: -1,
      name: "",
      heroId: -1,
    },
    player9: {
      xpos: -1,
      ypos: -1,
      name: "",
      heroId: -1,
    },
  }, // should contain location
  map_win: "",
};

function sendGameState(gameStateObject) {
  axios
    .post("http://127.0.0.1:8080/json", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
        Accept: "application/json",
      },
      // Stringify the payload into JSON:
      body: JSON.stringify(gameStateObject),
    })
    .then((res) => {
      console.log(res);
      if (res.ok) {
        return res.json();
      } else {
        console.log("something is wrong");
      }
    })
    .then((jsonResponse) => {
      // Log the response data in the console
      console.log(jsonResponse);
    })
    .catch((err) => console.error(err));
}

/* Game started/ended. - check
     Heroes alive/dead.
     Friendly structure HPs.

     Detecting player's:
         Position - check
         Team parity - check
         Player numbers and colors
         Heroes in match
         Fortification cooldown (?)

*/

function detectVisibilityTeamsOrPlayerOrSpectator(gsi) {
  if (
    gsi.player.hasOwnProperty("team2") ||
    gsi.player.hasOwnProperty("team3")
  ) {
    // Radiant (players 0-4) and Dire (players 0-5) visible
    global_gsi.team = "all";
  }

  if (
    !gsi.player.hasOwnProperty("team2") &&
    !gsi.player.hasOwnProperty("team3")
  ) {
    if (gsi.player.team_name === "spectator") {
      // Spectating a friend, no player coordinates visible
      global_gsi.team = "spectator";
    }
    // Individual player (unknown number?) visible
    if (gsi.player.team_name === "radiant") {
      global_gsi.team = "radiant";
    }

    if (gsi.player.team_name === "dire") {
      global_gsi.team = "dire";
    }
  }
}

/* Given a hero's JSON, player ID (0-9), and team, stores the x/y coordinate in the global json */
function capturePlayerData(heroJson, team, isCoordinateX, playerId) {
  if (global_gsi.team === "all") {
    let playerStr = "player" + playerId;
    let pos = isCoordinateX ? heroJson.xpos : heroJson.ypos;
    if (isCoordinateX) {
      global_gsi.players[playerStr].xpos = pos;
    } else {
      global_gsi.players[playerStr].ypos = pos;
    }
    // Name if not already set
    if (global_gsi.players[playerStr].name === "") {
      global_gsi.players[playerStr].name = heroJson.name;
    }
    // Id
    if (global_gsi.players[playerStr].heroId === -1) {
      global_gsi.players[playerStr].heroId = heroJson.id;
    }
    console.log(
      "Player " + playerId + (isCoordinateX ? " x" : " y") + ": " + pos
    );
  }
}

server.events.on("newclient", function (client) {
  console.log("New client connection, IP address: " + client.ip);

  if (client.auth && client.auth.token) {
    console.log("Auth token: " + client.auth.token);
  } else {
    console.log("No Auth token");
  }

  // Game start
  client.on("player:activity", function (activity) {
    if (activity === "playing") console.log("Connected!");
    console.log(activity);
    detectVisibilityTeamsOrPlayerOrSpectator(this.gamestate);
  });

  // Player team determined radiant or dire
  client.on("player:team_name", function (team_name) {
    console.log("Team: " + team_name);
    detectVisibilityTeamsOrPlayerOrSpectator(this.gamestate);
  });

  // Game end- "none" - not ended. Otherwise radiant or dire
  client.on("map:win_team", function (win_team) {
    console.log("Game won by team: " + win_team);
    global_gsi.map_win = win_team;
  });

  // Note: Sadly, if you are a player, it won't tell you which player ID you are (0 thru 9), so there's no clear way to
  // correlate who these coordinates are for unless you are on team 'all'.
  // Some crazy shenanigans goes on when I use a for loop for this, so I gave up in the name of AGILE DEVELOPMENT
  client.on("hero:team2:player0:xpos", function (xpos) {
    capturePlayerData(this.gamestate.hero["team2"]["player0"], 2, true, 0);
  });

  client.on("hero:team2:player0:ypos", function (ypos) {
    capturePlayerData(this.gamestate.hero["team2"]["player0"], 2, false, 0);
  });

  client.on("hero:team2:player1:xpos", function (xpos) {
    capturePlayerData(this.gamestate.hero["team2"]["player1"], 2, true, 1);
  });

  client.on("hero:team2:player1:ypos", function (ypos) {
    capturePlayerData(this.gamestate.hero["team2"]["player1"], 2, false, 1);
  });

  client.on("hero:team2:player2:xpos", function (xpos) {
    capturePlayerData(this.gamestate.hero["team2"]["player2"], 2, true, 2);
  });

  client.on("hero:team2:player2:ypos", function (ypos) {
    capturePlayerData(this.gamestate.hero["team2"]["player2"], 2, false, 2);
  });

  client.on("hero:team2:player3:xpos", function (xpos) {
    capturePlayerData(this.gamestate.hero["team2"]["player3"], 2, true, 3);
  });

  client.on("hero:team2:player3:ypos", function (ypos) {
    capturePlayerData(this.gamestate.hero["team2"]["player3"], 2, false, 3);
  });

  client.on("hero:team2:player4:xpos", function (xpos) {
    capturePlayerData(this.gamestate.hero["team2"]["player4"], 2, true, 4);
  });

  client.on("hero:team2:player4:ypos", function (ypos) {
    capturePlayerData(this.gamestate.hero["team2"]["player4"], 2, false, 4);
  });
  // Dire
  client.on("hero:team3:player5:xpos", function (xpos) {
    capturePlayerData(this.gamestate.hero["team3"]["player5"], 3, true, 5);
  });

  client.on("hero:team3:player5:ypos", function (ypos) {
    capturePlayerData(this.gamestate.hero["team3"]["player5"], 3, false, 5);
  });

  client.on("hero:team3:player6:xpos", function (xpos) {
    capturePlayerData(this.gamestate.hero["team3"]["player6"], 3, true, 6);
  });

  client.on("hero:team3:player6:ypos", function (ypos) {
    capturePlayerData(this.gamestate.hero["team3"]["player6"], 3, false, 6);
  });

  client.on("hero:team3:player7:xpos", function (xpos) {
    capturePlayerData(this.gamestate.hero["team3"]["player7"], 3, true, 7);
  });

  client.on("hero:team3:player7:ypos", function (ypos) {
    capturePlayerData(this.gamestate.hero["team3"]["player7"], 3, false, 7);
  });

  client.on("hero:team3:player8:xpos", function (xpos) {
    capturePlayerData(this.gamestate.hero["team3"]["player8"], 3, true, 8);
  });

  client.on("hero:team3:player8:ypos", function (ypos) {
    capturePlayerData(this.gamestate.hero["team3"]["player8"], 3, false, 8);
  });

  client.on("hero:team3:player9:xpos", function (xpos) {
    capturePlayerData(this.gamestate.hero["team3"]["player9"], 3, true, 9);
  });

  client.on("hero:team3:player9:ypos", function (ypos) {
    capturePlayerData(this.gamestate.hero["team3"]["player9"], 3, false, 9);
  });

  client.on("map:game_time", function (game_time) {
    // Polls game state for building data every 3 seconds.
    console.log(game_time);
    if (game_time % 5 === 0 && game_time > 10) {
      if (global_gsi.team === "") {
        detectVisibilityTeamsOrPlayerOrSpectator(this.gamestate);
      }

      if (global_gsi.team === "all") {
      }
      // Spectators can't see hero data, draft data. Only building data for some reason, for the team you are spectating
      if (global_gsi.team === "spectators") {
      }

      if (global_gsi.team === "radiant") {
      }

      if (global_gsi.team === " dire") {
      }
      global_gsi.building = this.gamestate.buildings;
      console.log("Building: " + this.gamestate.buildings);
    }
  });
});

// setInterval(sendGameState, 150);
