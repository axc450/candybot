# TODO: Make DB classmethods for these
class Candy:
    def __init__(self, id_, name, emoji, chance, text=None, command=None):
        self.id = id_
        self.name = name
        self.emoji = emoji
        self.chance = chance
        self.text = text
        self.command = command

    def __str__(self):
        return self.emoji

    def __repr__(self):
        return self.emoji

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return self.id


class CandyValue:
    def __init__(self, candy, value):
        self.candy = candy
        self.value = value

    def __repr__(self):
        return f"{self.value:,} {self.candy}"

    def __neg__(self):
        return CandyValue(self.candy, -self.value)

    def __radd__(self, other):
        if isinstance(other, CandyValue):
            value = other.value
        else:
            value = other
        return CandyValue(self.candy, self.value + value)

    @property
    def big_str(self):
        return f"{self.candy} x **{self.value:,}**"

    @property
    def small_str(self):
        return f"**{self.value:,}** {self.candy}"


class CandyCollection:
    def __init__(self, *items):
        self._items = list(items)

    def __repr__(self):
        return ", ".join(x.__repr__() for x in self._items)

    def __iadd__(self, candy_value):
        try:
            current_candy_value = next(x for x in self._items if x.candy == candy_value.candy)
            current_candy_value.value += candy_value.value
        except StopIteration:
            self._items.append(candy_value)
        return self

    def __neg__(self):
        return CandyCollection(*(-x for x in self._items))

    def __len__(self):
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __ge__(self, other):
        for candy_value in other:
            if candy_value.value > self[candy_value.candy]:
                return False
        return True

    def __getitem__(self, candy):
        return next((x.value for x in self._items if x.candy == candy), 0)

    @property
    def total(self):
        return sum(x.value for x in self._items)

    @property
    def list_str(self):
        return "\n".join(x.big_str for x in self._items if x.value is not 0)

    @property
    def line_str(self):
        return ", ".join(x.small_str for x in self._items if x.value is not 0)


class CandyDrop:
    def __init__(self, command, candy_value):
        self.command = command
        self.candy_value = candy_value

    @property
    def drop_str(self):
        if self.candy_value.candy.text:
            drop_text = self.candy_value.candy.text
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
