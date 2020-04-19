from typing import List
from candybot.engine import CandySettings, Candy


class Settings:
    def __init__(self, prefix, chance, pick_limit, min, max, cap, admins, blacklist, channels, candy):
        self.prefix = prefix
        self.chance = chance
        self.pick_limit = pick_limit
        self.min = min
        self.max = max
        self.cap = cap
        self.admins = admins
        self.blacklist = blacklist
        self.channels = channels
        self.candy: List[CandySettings] = candy

    def remove_candy(self, candy):
        candy_setting = next(x for x in self.candy if x.candy == candy)
        self.candy.remove(candy_setting)

    @classmethod
    def from_default(cls):
        candy = Candy("candy", "🍬")
        candy_settings = [CandySettings(candy, 1)]
        return cls(".", 0.2, 3, 5, 10, 100, [], [], [], candy_settings)

    @classmethod
    def from_json(cls, json):
        return cls(
            prefix=json["prefix"],
            chance=json["chance"],
            pick_limit=json["pick_limit"],
            min=json["min"],
            max=json["max"],
            cap=json["cap"],
            admins=json["admins"],
            blacklist=json["blacklist"],
            channels=json["channels"],
            candy=[CandySettings.from_json(x) for x in json["candy"]]
        )

    @property
    def to_json(self):
        return {
            "prefix": self.prefix,
            "chance": self.chance,
            "pick_limit": self.pick_limit,
            "min": self.min,
            "max": self.max,
            "cap": self.cap,
            "admins": self.admins,
            "blacklist": self.blacklist,
            "channels": self.channels,
            "candy": [x.to_json for x in self.candy]
        }

