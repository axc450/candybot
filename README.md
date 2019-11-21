<img src="https://i.imgur.com/MLNSv7V.png">

[![CircleCI](https://circleci.com/gh/axc450/CandyBot/tree/master.svg?style=svg)](https://circleci.com/gh/axc450/CandyBot/tree/master)
[![Discord](https://discordapp.com/api/guilds/302508083861520384/widget.png?style=shield)](https://discord.gg/4a6m5Kq)

**Holiday Event Bot for Discord**

## Adding to your Discord server

### Public

The easiest way to add CandyBot to your Discord server is to click [here](https://discordapp.com/api/oauth2/authorize?client_id=409047597572030484&permissions=8224&scope=bot). This will add the current version of CandyBot to a server you have permission to add bots to.

CandyBot requires the permissions `Manage Server` and `Manage Messages`. The above link should provide these. Without them, it will not function correctly.

### Private

You can host CandyBot yourself to have a private version of the bot. 

Requirements:
```
Python 3.7+
SQLite 3.24+
```

To run CandyBot yourself:

- Download a version of CandyBot [here](https://github.com/axc450/CandyBot/releases).
- If you want to run CandyBot from a different folder from where you extracted the ZIP, you can run `build/package.py` to generate another ZIP which just contains everything needed to run the bot which can then extract somewhere else.
- Run `pip install -r requirements.txt` to install everything the bot needs to run.
- Run `dbscripts/create.py` to create an empty database for CandyBot to use.
- Create a file called `token` which contains the Discord token for your bot.
- Start CandyBot with `python candybot`!

## For Developers

- You run CandyBot locally (ie. without a connection with Discord) by running `python candybot local`. This makes development much easier.  
- I recommend using PyCharm as an IDE. If you choose to do so, the full configuration is stored in the repo, so you just need to open the project and it should be ready out of the box.
- Any pull requests should be targeting `develop`.


## Credits

Created By:  
axc450 (Github) / Super#0010 (Discord)

Thanks to all donators & supporters of the project!  
Please consider donating [here](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=4MA3ZWKYSYNB6) to support CandyBot!
