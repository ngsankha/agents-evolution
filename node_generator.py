import random


def random_population(kinds):
    def fn():
        return random.choice(kinds)({'group': random.randrange(3)})
    return fn
