from candybot.engine import Stats, User, Settings, Shop
from candybot.interface import database, cache


class ReadRequest:
    def __init__(self, collection, server=None, one=False, fields=None, query=None):
        self.collection = collection
        self.server = server
        self.one = one
        self.fields = fields
        self.query = query


class WriteRequest:
    def __init__(self, collection, server, json):
        self.collection = collection
        self.server = server
        self.json = json


def get_settings(server):
    request = ReadRequest("settings", server=server, one=True)
    result = _get_data(request)
    if result:
        return Settings.from_json(result)
    settings = Settings.from_default()
    set_settings(server, settings)
    return settings


def set_settings(server, server_settings):
    request = WriteRequest("settings", server, server_settings.to_json)
    _set_data(request)


def get_user(server, user):
    request = ReadRequest("users", server=user, one=True)
    result = _get_data(request)
    return User.from_json(result, server) if result else User(user, server)


def set_user(user):
    request = WriteRequest("users", user.id, user.to_json)
    _set_data(request)


def get_users(server):
    request = ReadRequest("users", query={"invs": {"$elemMatch": {"server": server}}})
    # Always get all users via the database (ie do not cache)
    result = database.read(request)
    return [User.from_json(x, server) for x in result]


def get_shop(server) -> Shop:
    request = ReadRequest("shop", server=server, one=True)
    result = _get_data(request)
    if result:
        return Shop.from_json(result)
    shop = Shop.from_default()
    set_shop(server, shop)
    return shop


def set_shop(server, shop):
    request = WriteRequest("shop", server, shop.to_json)
    _set_data(request)


def get_stats(server) -> Stats:
    request = ReadRequest("stats", server=server, one=True)
    result = _get_data(request)
    if result:
        return Stats.from_json(result)
    stats = Stats.from_default()
    set_stats(server, stats)
    return stats


def set_stats(server, stats):
    request = WriteRequest("stats", server, stats.to_json)
    _set_data(request)


def get_donators():
    query = {}
    result = database.read("donators", query)
    return [x["tag"] for x in result]


def get_donators():
    request = ReadRequest("donators")
    result = _get_data(request)
    return [x["tag"] for x in result]


def _get_data(request):
    result = cache.read(request)
    if not result:
        result = database.read(request)
        request = WriteRequest(request.collection, request.server, result)
        cache.write(request)
    return result


def _set_data(request):
    database.write(request)
    cache.write(request)
