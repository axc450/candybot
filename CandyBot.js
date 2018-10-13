const discord   = require("discord.js")
const token     = require("./token.json")
const config    = require("./config.json")

const client    = new discord.Client()
var connected   = false

client.login(token["token"])

client.on("ready", () =>
{   
    client.user.setActivity("CandyBot v" + config["version"], {type: "PLAYING"})

    if (connected) {return}

    connected = true
    
    console.log("CandyBot Started!")
})
