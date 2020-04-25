from typing import List


class Candy:
    def __init__(self, name, emoji):
        self.name = name
        self.emoji = emoji

    def __str__(self):
        return self.emoji

    def __repr__(self):
        return self.emoji

    def __eq__(self, other):
        return (
            self.name == other.name and
            self.emoji == other.emoji
        )

    @classmethod
    def from_json(cls, json):
        return cls(
            name=json["name"],
            emoji=json["emoji"]
        )

    @property
    def to_json(self):
        return {
            "name": self.name,
            "emoji": self.emoji
        }


class CandySettings:
    def __init__(self, candy, chance=0, text=None, command=None):
        self.candy = candy
        self.chance = chance
        self.text = text
        self.command = command

    @classmethod
    def from_json(cls, json):
        return cls(
            candy=Candy.from_json(json["candy"]),
            chance=json["chance"],
            text=json["text"],
            command=json["command"]
        )

    @property
    def to_json(self):
        return {
            "candy": self.candy.to_json,
            "chance": self.chance,
            "text": self.text,
            "command": self.command
        }


class CandyValue:
    def __init__(self, candy, value):
        self.candy = candy
        self.value = value

    def __repr__(self):
        return self.small_str

    def __neg__(self):
        return CandyValue(self.candy, -self.value)

    def __copy__(self):
        return CandyValue(self.candy, self.value)

    def __add__(self, other):
        return CandyValue(self.candy, self.value + other)

    def __sub__(self, other):
        return CandyValue(self.candy, self.value - other)

    def __eq__(self, other):
        return (
            self.candy == other.candy and
            self.value == other.value
        )

    @property
    def big_str(self):
        return f"{self.candy} x **{self.value:,}**"

    @property
    def small_str(self):
        return f"**{self.value:,}** {self.candy}"

    @classmethod
    def from_json(cls, json):
        return cls(
            candy=Candy.from_json(json["candy"]),
            value=json["value"]
        )

    @property
    def to_json(self):
        return {
            "candy": self.candy.to_json,
            "value": self.value
        }


class CandyCollection:
    def __init__(self, *items):
        self._items: List[CandyValue] = list(items)

    def __repr__(self):
        return ", ".join(x.__repr__() for x in self._items)

    def __iadd__(self, other):
        if isinstance(other, CandyCollection):
            for candy_value in other:
                self += candy_value
        else:
            try:
                current_candy_value = next(x for x in self._items if x.candy == other.candy)
                current_candy_value.value += other.value
            except StopIteration:
                self._items.append(other)
        return self

    def __copy__(self):
        return CandyCollection(x.__copy__() for x in self._items)

    def __add__(self, other):
        new = CandyCollection()
        for candy_value in other:
            new += candy_value
        for candy_value in self:
            new += candy_value
        return new

    def __neg__(self):
        return CandyCollection(*(-x for x in self._items))

    def __len__(self):
        return len(self._items)

    def __bool__(self):
        return any(x.value for x in self._items)

    def __iter__(self):
        return iter(self._items)

    def __ge__(self, other):
        for candy_value in other:
            if candy_value.value > self[candy_value.candy]:
                return False
        return True

    def __getitem__(self, candy):
        return next((x.value for x in self._items if x.candy == candy), 0)

    def __setitem__(self, candy, value):
        try:
            current_candy_value = next(x for x in self._items if x.candy == candy)
            if value:
                current_candy_value.value = value
            else:
                self._items.remove(current_candy_value)
        except StopIteration:
            if value:
                self._items.append(CandyValue(candy, value))

    def __eq__(self, other):
        return self._items == list(other)

    @property
    def total(self):
        return sum(x.value for x in self._items)

    @property
    def list_str(self):
        return "\n".join(x.big_str for x in self._items if x.value is not 0)

    @property
    def line_str(self):
        sorted_candy = sorted(self._items, key=lambda x: x.value, reverse=True)
        return ", ".join(x.small_str for x in sorted_candy if x.value is not 0)

    @classmethod
    def from_json(cls, json):
        return cls(*[CandyValue.from_json(x) for x in json])

    @property
    def to_json(self):
        return [x.to_json for x in self._items]


class CandyDrop:
    def __init__(self, command, message, candy_value):
        self.command = command
        self.message = message
        self.candy_value = candy_value

    @property
    def drop_str(self):
        if self.message:
            drop_text = self.message
        else:
            drop_text = f"**Random {self.candy_value.candy.name} appeared!**"
        pick_text = f"_Type **{self.command.server_settings.prefix}{self.command.invocation}** to pick them up!_"
        border_size = max(len(drop_text), len(pick_text) - 6) // 3.5
        border = self.candy_value.candy.emoji * int(border_size)
        return f"{border}\n" \
               f"{drop_text}\n" \
               f"{pick_text}\n" \
               f"{border}"

    @property
    def pick_str(self):
        return f"You picked up {self.candy_value.small_str}!"
