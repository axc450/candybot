import sqlite3
from collections import defaultdict
from candybot.engine import Candy, CandyValue, CandyCollection, Shop, Settings


DB = None


def connect():
    global DB
    print("Connecting to the DB...")
    DB = sqlite3.connect("db")
    DB.execute("PRAGMA foreign_keys = ON")


def disconnect():
    print("Disconnecting from the DB...")
    DB.close()


# TODO: Can this be done in one statement?
def teardown(server):
    DB.execute("DELETE FROM INV WHERE server = ?", (server,))
    DB.execute("DELETE FROM SETTINGS_ADMINS WHERE server = ?", (server,))
    DB.execute("DELETE FROM SETTINGS_BLACKLIST WHERE server = ?", (server,))
    DB.execute("DELETE FROM SETTINGS_CANDY WHERE server = ?", (server,))
    DB.execute("DELETE FROM SETTINGS_CHANNELS WHERE server = ?", (server,))
    DB.execute("DELETE FROM SETTINGS_GENERAL WHERE server = ?", (server,))
    DB.execute("DELETE FROM SHOP WHERE server = ?", (server,))
    DB.execute("DELETE FROM STATS_CANDY WHERE server = ?", (server,))
    DB.execute("DELETE FROM STATS_SHOP WHERE server = ?", (server,))
    DB.commit()


def get_settings(server):
    query = "SELECT prefix, chance, pick_limit, min, max, cap FROM SETTINGS_GENERAL WHERE server = ?"
    row = DB.execute(query, (server,)).fetchone()
    return Settings(*row)


def get_channels(server):
    query = "SELECT channel FROM SETTINGS_CHANNELS WHERE server = ?"
    rows = DB.execute(query, (server,)).fetchall()
    return [row[0] for row in rows]


def get_admins(server):
    query = "SELECT admin FROM SETTINGS_ADMINS WHERE server = ?"
    rows = DB.execute(query, (server,)).fetchall()
    return [row[0] for row in rows]


def get_blacklist(server):
    query = "SELECT user FROM SETTINGS_BLACKLIST WHERE server = ?"
    rows = DB.execute(query, (server,)).fetchall()
    return [row[0] for row in rows]


def get_candy(server):
    query = "SELECT id, name, emoji, chance, message, command FROM SETTINGS_CANDY WHERE server = ?"
    rows = DB.execute(query, (server,)).fetchall()
    return [Candy(*row) for row in rows]


def get_inv(server, *users):
    # TODO: Why are we getting candy values we don't need? Also, improve this.
    query = "SELECT user, id, name, emoji, chance, message, command, value " \
            "FROM INV a JOIN SETTINGS_CANDY b ON a.candy = b.id " \
            "WHERE a.server = ? AND b.server = ?"
    if users:
        query += f" AND user IN ({', '.join('?' * len(users))})"
    rows = DB.execute(query, (server, server, *users)).fetchall()
    invs = defaultdict(CandyCollection)
    for row in rows:
        candy = Candy(*row[1:-1])
        candy_value = CandyValue(candy, row[-1])
        user = row[0]
        invs[user] += candy_value
    return invs


def get_shop(server):
    query = "SELECT role, id, name, emoji, chance, value " \
            "FROM SHOP a JOIN SETTINGS_CANDY b ON a.candy = b.id " \
            "WHERE a.server = ? AND b.server = ?"
    rows = DB.execute(query, (server, server)).fetchall()
    return Shop.from_db(rows)


def get_donators():
    query = "SELECT tag FROM DONATORS"
    rows = DB.execute(query).fetchall()
    return [row[0] for row in rows]


def get_stats_candy(server):
    query = "SELECT a.id, name, emoji, chance, message, command, value " \
            "FROM STATS_CANDY a JOIN SETTINGS_CANDY b ON a.id = b.id " \
            "WHERE a.server = ? AND b.server = ?"
    rows = DB.execute(query, (server, server)).fetchall()
    return CandyCollection(*[CandyValue(Candy(*row[:-1]), row[-1]) for row in rows])


def get_stats_shop(server):
    query = "SELECT value " \
            "FROM STATS_SHOP " \
            "WHERE server = ?"
    row = DB.execute(query, (server,)).fetchone()
    return 0 if not row else row[0]


def set_settings(server, prefix, chance, pick_limit, min_, max_, cap):
    query = "INSERT INTO SETTINGS_GENERAL " \
            "VALUES(?, ?, ?, ?, ?, ?, ?)"
    DB.execute(query, (server, prefix, chance, pick_limit, min_, max_, cap))
    DB.commit()


def set_settings_chance(server, chance):
    query = "UPDATE SETTINGS_GENERAL " \
            "SET chance = ? " \
            "WHERE server = ?"
    DB.execute(query, (chance, server))
    DB.commit()


def set_settings_prefix(server, prefix):
    query = "UPDATE SETTINGS_GENERAL " \
            "SET prefix = ? " \
            "WHERE server = ?"
    DB.execute(query, (prefix, server))
    DB.commit()


def set_settings_min(server, amount):
    query = "UPDATE SETTINGS_GENERAL " \
            "SET min = ? " \
            "WHERE server = ?"
    DB.execute(query, (amount, server))
    DB.commit()


def set_settings_max(server, amount):
    query = "UPDATE SETTINGS_GENERAL " \
            "SET max = ? " \
            "WHERE server = ?"
    DB.execute(query, (amount, server))
    DB.commit()


def set_settings_cap(server, amount):
    query = "UPDATE SETTINGS_GENERAL " \
            "SET cap = ? " \
            "WHERE server = ?"
    DB.execute(query, (amount, server))
    DB.commit()


def set_settings_candy_add(server, name, emoji, chance=0):
    query = "INSERT INTO SETTINGS_CANDY VALUES (?, " \
            "IFNULL((SELECT MAX(id)+1 FROM SETTINGS_CANDY WHERE server = ?), 0), " \
            "?, ?, ?, NULL, NULL)"
    DB.execute(query, (server, server, name, emoji, chance))
    DB.commit()


def set_settings_candy_remove(server, candy):
    query = "DELETE FROM SETTINGS_CANDY WHERE server = ? AND id = ?"
    DB.execute(query, (server, candy))
    DB.commit()


def set_settings_candy_chance(server, candy, chance):
    query = "UPDATE SETTINGS_CANDY " \
            "SET chance = ? " \
            "WHERE server = ? AND id = ?"
    DB.execute(query, (chance, server, candy))
    DB.commit()


def set_settings_candy_message(server, candy, message):
    query = "UPDATE SETTINGS_CANDY " \
            "SET message = ? " \
            "WHERE server = ? AND id = ?"
    DB.execute(query, (message, server, candy))
    DB.commit()


def set_settings_candy_command(server, candy, command):
    query = "UPDATE SETTINGS_CANDY " \
            "SET command = ? " \
            "WHERE server = ? AND id = ?"
    DB.execute(query, (command, server, candy))
    DB.commit()


def set_blacklist(server, user, remove=False):
    if remove:
        query = "DELETE FROM SETTINGS_BLACKLIST " \
                "WHERE server = ? and user = ?"
    else:
        query = "INSERT INTO SETTINGS_BLACKLIST " \
                "VALUES (?, ?)"
    DB.execute(query, (server, user))
    DB.commit()


def set_admin(server, admin, remove=False):
    if remove:
        query = "DELETE FROM SETTINGS_ADMINS " \
                "WHERE server = ? and admin = ?"
    else:
        query = "INSERT INTO SETTINGS_ADMINS " \
                "VALUES (?, ?)"
    DB.execute(query, (server, admin))
    DB.commit()


def set_channel(server, channel, remove=False):
    if remove:
        query = "DELETE FROM SETTINGS_CHANNELS " \
                "WHERE server = ? and channel = ?"
    else:
        query = "INSERT INTO SETTINGS_CHANNELS " \
                "VALUES (?, ?)"
    DB.execute(query, (server, channel))
    DB.commit()


def set_inv(server, user, candy, update=False):
    query = "INSERT OR REPLACE INTO INV VALUES(?, ?, ?, ?) ON " \
            "CONFLICT(server, user, candy) DO UPDATE SET value ="
    if update:
        query += " value + ?"
    else:
        query += " ?"
    if isinstance(candy, CandyValue):
        params = [(server, user, candy.candy.id, candy.value, candy.value)]
    elif isinstance(candy, CandyCollection):
        params = [(server, user, x.candy.id, x.value, x.value) for x in candy]
    else:
        raise TypeError
    DB.executemany(query, params)
    DB.commit()


def set_shop_cost(server, role, candy, value):
    if value:
        query = "INSERT OR REPLACE INTO SHOP VALUES(?, ?, ?, ?) ON " \
                "CONFLICT(server, role, candy) DO UPDATE SET value = ?"
        DB.execute(query, (server, role, candy.id, value, value))
    else:
        query = "DELETE FROM SHOP " \
                "WHERE server = ? AND role = ? AND candy = ?"
        DB.execute(query, (server, role, candy.id))
    DB.commit()


def set_stats_candy(server, candy):
    query = "INSERT OR REPLACE INTO STATS_CANDY VALUES(?, ?, ?) ON " \
            "CONFLICT(server, id) DO UPDATE SET value = value + ?"
    DB.execute(query, (server, candy.candy.id, candy.value, candy.value))
    DB.commit()


def set_stats_shop(server):
    query = "INSERT OR REPLACE INTO STATS_SHOP VALUES(?, 1) ON " \
            "CONFLICT(server) DO UPDATE SET value = value + 1"
    DB.execute(query, (server,))
    DB.commit()
