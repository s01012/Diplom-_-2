import random

def generate_random_email():
    alphabet = [chr(i) for i in range(97, 123)]
    return ''.join(random.sample(alphabet, 4)) + f'_test_{random.randint(100, 999)}@mail.com'

def generate_random_password():
    return random.randint(100000, 999999)

def generate_random_name():
    alphabet = [chr(i) for i in range(97, 123)]
    return ''.join(random.sample(alphabet, 4)) + f'_test_{random.randint(100, 999)}'