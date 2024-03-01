import random


def choose_random_home_world(home_worlds):
    return random.choices(population=home_worlds, weights=[world.roll_weight for world in home_worlds], k=1)[0]
