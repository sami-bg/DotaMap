var d2gsi = require("dota2-gsi");
var server = new d2gsi();
const axios = require("axios").default;

var global_gsi = {team: "", building: {}, players: {}}

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
      if (gsi.player.hasOwnProperty('team2') || gsi.player.hasOwnProperty('team3')) {
        // Radiant (players 0-4) and Dire (players 0-5) visible
        global_gsi.team = "all";
      }

      if (!gsi.player.hasOwnProperty('team2') && !gsi.player.hasOwnProperty('team3')) {
        if (gsi.player.team_name === 'spectator') {
          // Spectating a friend, no player coordinates visible
          global_gsi.team = "spectator";
        }
        // Individual player (unknown number?) visible
        if (gsi.player.team_name === 'radiant') {
          global_gsi.team = "radiant";
        }

        if (gsi.player.team_name === 'dire') {
          global_gsi.team = "dire";
        }
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
    global_gsi.team = team_name;
  });

  // Game end- "none" - not ended. Otherwise radiant or dire
  client.on("map:win_team", function (win_team) {
    console.log("Game won by team: " + win_team);
  });

  client.on("hero:xpos", function (xpos) {
    console.log("Hero x position: " + xpos);
  })

  client.on("hero:ypos", function (ypos) {
    console.log("Hero y position: " + ypos)
  })
  // TODO
  client.on("map:game_time", function (game_time) {
    // Polls game state for building data every 3 seconds.
    if (game_time % 3 === 0) {
      if (global_gsi.team === "") {
        detectVisibilityTeamsOrPlayerOrSpectator(this.gamestate);
      }

      if (global_gsi.team === "all") {

      }

      if (global_gsi.team === "spectators") {

      }

      if (global_gsi.team === "radiant") {

      }

      if (global_gsi.team === " dire") {

      }

      console.log("Building: " + this.gamestate.buildings[global_gsi.team])
    }

  })

});
