from candybot.engine import CandyCollection


class Stats:
    def __init__(self, candy_dropped, shop_items_bought):
        self.candy_dropped = candy_dropped
        self.shop_items_bought = shop_items_bought

    def remove_candy(self, candy):
        self.candy_dropped[candy] = 0

    @classmethod
    def from_default(cls):
        return cls(CandyCollection(), 0)

    @classmethod
    def from_json(cls, json):
        return cls(
            candy_dropped=CandyCollection.from_json(json["candy_dropped"]),
            shop_items_bought=json["shop_items_bought"]
        )

    @property
    def to_json(self):
        return {
            "candy_dropped": self.candy_dropped.to_json,
            "shop_items_bought": self.shop_items_bought
        }
