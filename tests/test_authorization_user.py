import allure
import random
import requests
from utils.url import *
from utils.endpoint import *
from utils.test_data import *


class TestAuthorizationUser:
    dict_registration = {}

    @classmethod
    def setup_class(cls):
        alphabet = [chr(i) for i in range(97, 123)]
        cls.dict_registration = {
            'email': (''.join(random.sample(alphabet, 4)) + f'_test_{random.randint(100, 999)}@mail.com'),
            'password': random.randint(100000, 999999),
            'name': (''.join(random.sample(alphabet, 4)) + f'_test_{random.randint(100, 999)}')
        }
        requests.post(f'{GetUrl.URL}{Endpoint.CREATE_USER}', data=cls.dict_registration)

    @allure.title('Отправляем POST запрос для авторизации ранее зарегистрированного пользователя')
    def test_authorization_user(self):
        payload = {
            'email': self.dict_registration.get('email'),
            'password': self.dict_registration.get('password')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.LOGIN_USER}', data=payload)
        response_body = response.json()
        assert response.status_code == 200 and response_body.get('success') == True and 'user' in response_body

    @allure.title('Отправляем POST запрос для авторизации пользователя с несуществующим e-mail и паролем')
    def test_authorization_user_non_existent_email_and_password(self):
        gen_data = generator()
        payload = {
            'email': gen_data.get('email'),
            'password': gen_data.get('password')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.LOGIN_USER}', data=payload)
        response_body = response.json()
        assert (response.status_code == 401 and response_body.get('success') == False
                and response_body.get('message')) == 'email or password are incorrect'

    @classmethod
    def teardown_class(cls):
        cls.payload = {
            'email': cls.dict_registration.get('email'),
            'password': cls.dict_registration.get('password'),
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.LOGIN_USER}', data=cls.payload)
        response_body = response.json()
        requests.delete(f'{GetUrl.URL}{Endpoint.DELETE_USER}',
                        headers={'Authorization': f'{response_body.get("accessToken")}'})
