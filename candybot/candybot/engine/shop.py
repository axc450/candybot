from candybot.engine import Candy, CandyValue, CandyCollection


class Shop:
    def __init__(self, items):
        self.items = items

    def __getitem__(self, item):
        return self.items[item]

    @classmethod
    def from_db(cls, rows):
        items = []
        for row in rows:
            role = row[0]
            candy = Candy(row[1], row[2], row[3], row[4])
            cost = CandyValue(candy, row[5])
            try:
                shop_item = next(x for x in items if x.item == role)
                shop_item.cost += cost
            except StopIteration:
                items.append(ShopItem(role, CandyCollection(cost)))
        return cls(items)


class ShopItem:
    def __init__(self, item, cost):
        self.item = item
        self.cost = cost
