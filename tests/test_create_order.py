import allure
import random
import requests
from utils.url import *
from utils.endpoint import *
from utils.test_data import *


class TestCreateOrder:
    dict_registration = {}

    @classmethod
    def setup_class(cls):
        alphabet = [chr(i) for i in range(97, 123)]
        cls.dict_registration = {
            'email': (''.join(random.sample(alphabet, 4)) + f'_test_{random.randint(100, 999)}@mail.com'),
            'password': random.randint(100000, 999999),
            'name': (''.join(random.sample(alphabet, 4)) + f'_test_{random.randint(100, 999)}')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_USER}', data=cls.dict_registration)
        cls.response_body = response.json()

    @allure.title('Отправляем POST запрос на создание заказа у авторизованного пользователя')
    def test_create_order_with_authorization(self):
        r = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_ORDER}',
                           headers={'Authorization': f'{self.response_body.get("accessToken")}'}, data=exact_ingredients)
        r_body = r.json()
        assert r.status_code == 200 and r_body.get('success') == True

    @allure.title('Отправляем POST запрос на создание заказа у неавторизованного пользователя')
    def test_create_order_with_not_authorization(self):
        r = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_ORDER}', data=exact_ingredients)
        r_body = r.json()
        assert r.status_code == 200 and r_body.get('success') == True

    @allure.title('Отправляем POST запрос на создание заказа БЕЗ ингредиентов, у авторизованного пользователя')
    def test_create_order_with_authorization_and_not_ingredient(self):
        r = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_ORDER}',
                           headers={'Authorization': f'{self.response_body.get("accessToken")}'})
        r_body = r.json()
        print(r_body)
        assert (r.status_code == 400 and r_body.get('success') == False
                and r_body.get('message') == 'Ingredient ids must be provided')

    @allure.title('Отправляем POST запрос на создание заказа c несуществующими ингредиентами в системе, '
                  'будучи авторизованным пользователем')
    def test_create_order_with_authorization_and_not_exact_ingredient(self):
        r = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_ORDER}',
                           headers={'Authorization': f'{self.response_body.get("accessToken")}'},
                          data=not_exact_ingredients)

        assert r.status_code == 500 and "text/html" in r.headers.get("Content-Type", "")

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