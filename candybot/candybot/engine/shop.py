from typing import List
from candybot.engine import CandyCollection


class Shop:
    def __init__(self, items):
        self.roles: List[Role] = items
        self._all = self.roles

    def __getitem__(self, item):
        return self._all[item - 1]

    def __iter__(self):
        return iter(self._all)

    def __len__(self):
        return len(self._all)

    def remove_item(self, item):
        del self._all[item - 1]

    def remove_candy(self, candy):
        for item in list(self):
            item.remove_candy(candy)

    @classmethod
    def from_default(cls):
        return cls([])

    @classmethod
    def from_json(cls, json):
        return cls([Role.from_json(x) for x in json["roles"]])

    @property
    def to_json(self):
        return {
            "roles": [x.to_json for x in self.roles]
        }


class Role:
    def __init__(self, item, cost=None):
        self.item = item
        self.cost: CandyCollection = cost if cost else CandyCollection()

    def remove_candy(self, candy):
        self.cost[candy] = 0

    @classmethod
    def from_json(cls, json):
        return cls(
            item=json["item"],
            cost=CandyCollection.from_json(json["cost"])
        )

    @property
    def to_json(self):
        return {
            "item": self.item,
            "cost": self.cost.to_json
        }
