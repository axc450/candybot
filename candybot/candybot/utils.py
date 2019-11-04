import random


def get_value(min_, max_):
    return random.randint(min_, max_)


def roll(chance):
    return random.random() <= chance


def get_choice(values, weights):
    return random.choices(values, weights)[0]


# TODO: Handle division by 0
def chance_value_to_percent(values, total=None):
    if not total:
        total = sum(x.chance for x in values)
    return {x: (x.chance / total) * 100 for x in values}
