from typing import List
from candybot.engine import CandyCollection, CandyValue, Candy


class Shop:
    def __init__(self, roles, conversions, upgrades):
        self.roles: List[Role] = roles
        self.conversions: List[Conversion] = conversions
        self.upgrades: List[Upgrade] = upgrades
        self._all = roles + conversions + upgrades

    def __getitem__(self, item):
        return self._all[item - 1]

    def __iter__(self):
        return iter(self._all)

    def __len__(self):
        return len(self._all)

    @property
    def all(self):
        i = 1
        result = {"roles": [], "conversions": [], "upgrades": []}
        for item in self.roles:
            result["roles"].append((i, item))
            i += 1
        for item in self.conversions:
            result["conversions"].append((i, item))
            i += 1
        for item in self.upgrades:
            result["upgrades"].append((i, item))
            i += 1
        return result

    def remove_item(self, item):
        del self._all[item - 1]

    def remove_candy(self, candy):
        for item in self._all:
            item.remove_candy(candy)

    @classmethod
    def from_default(cls):
        return cls([], [], [])

    @classmethod
    def from_json(cls, json):
        return cls(
            [Role.from_json(x) for x in json["roles"]],
            [Conversion.from_json(x) for x in json["conversions"]],
            [Upgrade.from_json(x) for x in json["upgrades"]]
        )

    @property
    def to_json(self):
        return {
            "roles": [x.to_json for x in self.roles],
            "conversions": [x.to_json for x in self.conversions],
            "upgrades": [x.to_json for x in self.upgrades]
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


class Conversion:
    def __init__(self, candy_value, cost=None):
        self.candy_value: CandyValue = candy_value
        self.cost: CandyCollection = cost if cost else CandyCollection()

    def __str__(self):
        return f"{self.cost.line_str} :arrow_right: {self.candy_value.small_str}"

    @classmethod
    def from_json(cls, json):
        return cls(
            candy_value=CandyValue.from_json(json["candy_value"]),
            cost=CandyCollection.from_json(json["cost"])
        )

    @property
    def to_json(self):
        return {
            "candy_value": self.candy_value.to_json,
            "cost": self.cost.to_json
        }


class Upgrade:
    def __init__(self, candy, cost=None):
        self.candy: Candy = candy
        self.cost: CandyCollection = cost if cost else CandyCollection()

    def __str__(self):
        return f"{self.cost.line_str} :arrow_right: {self.candy}"

    @classmethod
    def from_json(cls, json):
        return cls(
            candy=Candy.from_json(json["candy"]),
            cost=CandyCollection.from_json(json["cost"])
        )

    @property
    def to_json(self):
        return {
            "candy": self.candy.to_json,
            "cost": self.cost.to_json
        }
