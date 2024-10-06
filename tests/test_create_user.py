import allure
import random
import requests
from utils.url import *
from utils.endpoint import *


class TestCreateUser:
    dict_registration = {}

    @classmethod
    def setup_class(cls):
        alphabet = [chr(i) for i in range(97, 123)]
        cls.dict_registration = {
            'email': (''.join(random.sample(alphabet, 4)) + f'_test_{random.randint(100, 999)}@mail.com'),
            'password': random.randint(100000, 999999),
            'name': (''.join(random.sample(alphabet, 4)) + f'_test_{random.randint(100, 999)}')
        }

    @allure.title('Отправляем POST запрос на создание пользователя с неиспользованными ранее данными')
    def test_create_user(self):
        payload = {
            'email': self.dict_registration.get('email'),
            'password': self.dict_registration.get('password'),
            'name': self.dict_registration.get('name')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_USER}', data=payload)
        response_body = response.json()
        assert response.status_code == 200 and response_body.get('success') == True and 'user' in response_body

    @allure.title('Отправляем POST запрос на создание пользователя с данными, которые уже есть в системе')
    def test_create_identical_user(self):
        payload = {
            'email': self.dict_registration.get('email'),
            'password': self.dict_registration.get('password'),
            'name': self.dict_registration.get('name')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_USER}', data=payload)
        response_body = response.json()
        assert (response.status_code == 403 and response_body.get('success') == False
                and response_body.get('message')) == 'User already exists'

    @allure.title('Отправляем POST запрос на создание пользователя без пароля')
    def test_create_user_without_password(self):
        payload = {
            'email': self.dict_registration.get('email'),
            'password': '',
            'name': self.dict_registration.get('name')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_USER}', data=payload)
        response_body = response.json()
        assert (response.status_code == 403 and response_body.get('success') == False
                and response_body.get('message')) == 'Email, password and name are required fields'

    @classmethod
    def tear_down(cls):
        cls.payload = {
            'email': cls.dict_registration.get('email'),
            'password': cls.dict_registration.get('password'),
            'name': cls.dict_registration.get('name')
        }
        response = requests.delete(f'{GetUrl.URL}{Endpoint.CREATE_USER}', data=cls.payload)
        response_body = response.json()
        requests.delete(f'{GetUrl.URL}{Endpoint.CREATE_USER}', headers={'Authorization': f'{response_body.get("accessToken")}'})
