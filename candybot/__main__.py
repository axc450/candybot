import sys
from candybot.clients import local, live
from candybot.interface import database
from candybot import files

VERSION = files.load_version()
SETTINGS = files.load_settings()

print(f"CandyBot {VERSION}")

database.connect(SETTINGS["db_connection_string"], SETTINGS["db_database"])

if len(sys.argv) > 1 and sys.argv[1] == "local":
    local.start()
else:
    live.start()

database.disconnect()
