import random
import requests
from datetime import datetime

print('ddsdsdsd')


def generator():
    alphabet = [chr(i) for i in range(97, 123)]

    dict_registration = {
        'email': (''.join(random.sample(alphabet, 4)) + f'_test_{random.randint(100, 999)}@mail.com'),
        'password': random.randint(100000, 999999),
        'name': (''.join(random.sample(alphabet, 4)) + f'_test_{random.randint(100, 999)}')
    }
    return dict_registration


exact_ingredients = {
    'ingredients': ['61c0c5a71d1f82001bdaaa71', '61c0c5a71d1f82001bdaaa70', '61c0c5a71d1f82001bdaaa72']
}

not_exact_ingredients = {
    'ingredients': ['61c0c5adsdd71d1f82001bdaaa7f', '5fc0c5a71d1f8dsddd2001bdaaa73', '61c0c5a71d1f8200dsdsd1bdaab99']
}
