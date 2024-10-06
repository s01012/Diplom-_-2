import random
from datetime import datetime


def generator():
    alphabet = [chr(i) for i in range(97, 123)]

    dict_registration = {
        'email': (''.join(random.sample(alphabet, 4)) + f'_test_{random.randint(100, 999)}@mail.com'),
        'password': random.randint(100000, 999999),
        'name': (''.join(random.sample(alphabet, 4)) + f'_test_{random.randint(100, 999)}')
    }
    return dict_registration

