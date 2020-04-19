import random


def get_value(min, max):
    return random.randint(min, max)


def roll(chance):
    return random.random() <= chance


def get_choice(values, weights):
    return random.choices(values, weights)[0]


def chance_value_to_percent(candy_settings, candy=None):
    total = sum(x.chance for x in candy_settings)
    if not total:
        result = [(x.candy, 0) for x in candy_settings]
    else:
        result = [(x.candy, (x.chance / total) * 100) for x in candy_settings]
    if candy:
        return next(x for x in result if x[0] == candy)[1]
    return result
