var d2gsi = require('dota2-gsi');
var server = new d2gsi();
const axios = require('axios').default;
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
var cars = [{"make":"Porsche", "model":"911S"}]
axios.post("http://127.0.0.1:8080/json",
 {
 method: 'POST',
 headers: {
 'Content-type': 'application/json',
 'Accept': 'application/json'
 },
     // Strigify the payload into JSON:
 body:JSON.stringify(cars)}).then(res=>{
          console.log(res)
 if(res.ok){
 return res.json()
 }else{
    console.log("something is wrong")
 }
 }).then(jsonResponse=>{

 // Log the response data in the console
 console.log(jsonResponse)
 }
 ).catch((err) => console.error(err));

server.events.on('newclient', function(client) {
    console.log("New client connection, IP address: " + client.ip);
    if (client.auth && client.auth.token) {
        console.log("Auth token: " + client.auth.token);
    } else {
        console.log("No Auth token");
    }

    client.on('player:activity', function(activity) {
        if (activity == 'playing') console.log("Game started!");
    });
    client.on('hero:level', function(level) {
        var a = JSON.stringify({ "name": name.value, "email": email.value });
        console.log("Now level " + level);

    });
    client.on('abilities:ability0:can_cast', function(can_cast) {
        if (can_cast) console.log("Ability0 off cooldown!");
    });
});