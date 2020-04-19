from typing import List
from candybot.engine import CandyCollection


class Shop:
    def __init__(self, items):
        self.items: List[ShopItem] = items

    def __getitem__(self, item):
        return self.items[item - 1]

    def remove_candy(self, candy):
        for item in self.items:
            item.remove_candy(candy)

    @classmethod
    def from_default(cls):
        return cls([])

    @classmethod
    def from_json(cls, json):
        return cls([ShopItem.from_json(x) for x in json["items"]])

    @property
    def to_json(self):
        return {
            "items": [x.to_json for x in self.items]
        }


class ShopItem:
    def __init__(self, item, cost):
        self.item = item
        self.cost: CandyCollection = cost

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
