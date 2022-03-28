import string
import random


def random_number(length: int = 10):
    return "".join([random.choice(string.digits) for _ in range(length)])
    
