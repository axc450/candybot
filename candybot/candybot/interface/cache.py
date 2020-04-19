class SubCache:
    def __init__(self):
        self._items = {}

    def __getitem__(self, item):
        return self._items.get(item)

    def __setitem__(self, key, value):
        self._items[key] = value


class Cache:
    def __init__(self):
        self.settings = SubCache()
        self.users = SubCache()
        self.shop = SubCache()
        self.stats = SubCache()
        self.donators = SubCache()

    def __getitem__(self, item):
        return getattr(self, item)


_CACHE = Cache()


def read(request):
    return _CACHE[request.collection][request.server]


def write(request):
    _CACHE[request.collection][request.server] = request.json
