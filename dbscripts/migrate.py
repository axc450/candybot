import sqlite3

NAME = "db"

db = sqlite3.connect(NAME)
v = db.execute(f"PRAGMA user_version").fetchone()[0]

db.close()
