import random


def generate_random_key():
    # Ensures the returned number is always 5 numbers long.
    return random.randint(10000, 99999)
