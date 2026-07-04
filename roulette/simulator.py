import random

RED_NUMBERS = {1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36}
BLACK_NUMBERS = {2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35}

COLUMNS = {
    1: {1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34},
    2: {2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35},
    3: {3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36},
}

DOZENS = {
    1: set(range(1, 13)),
    2: set(range(13, 25)),
    3: set(range(25, 37)),
}


def spin_wheel(seed=None):
    if seed is not None:
        random.seed(seed)
    return random.randint(0, 36)

#   Ako zatreba
def get_color(number):
    if number in RED_NUMBERS:
        return 'red'
    elif number in BLACK_NUMBERS:
        return 'black'
    return 'green'  # 0