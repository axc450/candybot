"""
Migrates a CandyBot SQL database into a Mongo Database
"""

import sqlite3

from __main__ import SETTINGS
from candybot import data
from candybot.interface import database


# Connect to databases
sql = sqlite3.connect("db")
database.connect(SETTINGS["db_connection_string"], SETTINGS["db_database"])

# TODO: Make migration script

sql.close()
