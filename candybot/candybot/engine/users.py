from candybot.engine import CandyCollection


class User:
    def __init__(self, id, server, invs=None):
        self.id = id
        self._server = server
        self._invs = invs if invs else []
        try:
            self.inv = next(x.inv for x in self._invs if x.server == server)
        except StopIteration:
            inv = Inventory(server)
            self._invs.append(inv)
            self.inv = inv.inv

    def remove_inv(self):
        inv = next(x for x in self._invs if x.server == self._server)
        self._invs.remove(inv)

    @classmethod
    def from_json(cls, json, server):
        return cls(
            id=json["_id"],
            invs=[Inventory.from_json(x) for x in json["invs"]],
            server=server
        )

    @property
    def to_json(self):
        return {
            "_id": self.id,
            "invs": [x.to_json for x in self._invs]
        }


class Inventory:
    def __init__(self, server, inv=None):
        self.server = server
        self.inv = inv if inv else CandyCollection()

    @classmethod
    def from_json(cls, json):
        return cls(
            server=json["server"],
            inv=CandyCollection.from_json(json["inv"])
        )

    @property
    def to_json(self):
        return {
            "server": self.server,
            "inv": self.inv.to_json
        }
