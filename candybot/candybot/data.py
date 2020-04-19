from candybot.engine import Stats, User, Settings, Shop
from candybot.interface import database


def get_settings(server):
    query = {"_id": server}
    result = database.read("settings", query, one=True)
    if result:
        return Settings.from_json(result)
    settings = Settings.from_default()
    set_settings(server, settings)
    return settings


def set_settings(server, server_settings):
    query = {"_id": server}
    document = {"$set": server_settings.to_json}
    database.write("settings", query, document, one=True)


def get_user(server, user):
    query = {"_id": user, "invs": {"$elemMatch": {"server": server}}}
    result = database.read("users", query, one=True)
    return User.from_json(result, server) if result else User(user, server)


def set_user(user):
    query = {"_id": user.id}
    document = {"$set": user.to_json}
    database.write("users", query, document, one=True)


def get_users(server):
    query = {"invs": {"$elemMatch": {"server": server}}}
    result = database.read("users", query)
    return [User.from_json(x, server) for x in result]


# def reset_users(server):
#     query = {}
#     document = {"$pull": {"invs": {"server": server}}}
#     database.write("users", query, document)


def get_shop(server) -> Shop:
    query = {"_id": server}
    result = database.read("shop", query, one=True)
    if result:
        return Shop.from_json(result)
    shop = Shop.from_default()
    set_shop(server, shop)
    return shop


def set_shop(server, shop):
    query = {"_id": server}
    document = {"$set": shop.to_json}
    database.write("shop", query, document, one=True)


def get_stats(server) -> Stats:
    query = {"_id": server}
    result = database.read("stats", query, one=True)
    if result:
        return Stats.from_json(result)
    stats = Stats.from_default()
    set_settings(server, stats)
    return stats


def set_stats(server, stats):
    query = {"_id": server}
    document = {"$set": stats.to_json}
    database.write("stats", query, document, one=True)


def get_donators():
    query = {}
    result = database.read("donators", query)
    return [x["tag"] for x in result]
