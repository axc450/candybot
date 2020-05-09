import sys
from candybot.clients import local, live
from candybot.interface import database, files

VERSION = "v" + files.load_file("version", "Could not find a CandyBot version!")
SETTINGS = files.load_file("settings.json", "Could not load the settings file!", is_json=True)

print(f"CandyBot {VERSION}")

database.connect(SETTINGS["db_connection_string"], SETTINGS["db_database"])

if len(sys.argv) > 1 and sys.argv[1] == "local":
    local.start()
else:
    live.start()

database.disconnect()
