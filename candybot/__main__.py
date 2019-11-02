import sys
from candybot.clients import local, live
from candybot.interface import database, files

VERSION = files.load_version()

print(f"CandyBot {VERSION}")

database.connect()

if len(sys.argv) > 1 and sys.argv[1] == "local":
    local.start()
else:
    live.start()

database.disconnect()
