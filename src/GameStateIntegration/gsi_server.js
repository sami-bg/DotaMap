var d2gsi = require("dota2-gsi");
var server = new d2gsi();
const axios = require("axios").default;

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

/* Game started/ended.
     Heroes alive/dead.
     Friendly structure HPs.

     Detecting player's:
         Position
         Team parity
         Player numbers and colors
         Heroes in match
         Fortification cooldown (?)
*/


server.events.on("newclient", function (client) {

  console.log("New client connection, IP address: " + client.ip);

  if (client.auth && client.auth.token) {
    console.log("Auth token: " + client.auth.token);
  } else {
    console.log("No Auth token");
  }

  client.on("player:activity", function (activity) {
    if (activity == "playing") console.log("Game started!");
  });

  client.on("", function (activity) {

  });

  client.on("hero:level", function (level) {
    console.log(level);
    console.log("Now level " + level);
  });

  client.on("abilities:ability0:can_cast", function (can_cast) {
    if (can_cast) console.log("Ability0 off cooldown!");
  });

  client.on("hero:xpos", function (xpos) {
    console.log("Hero x position: " + xpos)
  })

  client.on("hero:ypos", function (ypos) {
    console.log("Hero y position: " + ypos)
  })

});
