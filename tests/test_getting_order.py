import allure
import random
import requests
from utils.url import *
from utils.endpoint import *
from utils.test_data import *


class TestGettingOrder:
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

    @allure.title('Получаем заказ(ы) авторизованного пользователя')
    def test_getting_order_with_authorization(self):
        response_create_order = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_ORDER}',
                           headers={'Authorization': f'{self.response_body.get("accessToken")}'}, data=exact_ingredients)
        response_body_create_order = response_create_order.json()
        response_getting_order = requests.get(f'{GetUrl.URL}{Endpoint.GET_ORDER}',
                           headers={'Authorization': f'{self.response_body.get("accessToken")}'})
        response_body_getting_order = response_getting_order.json()
        assert (response_getting_order.status_code == 200
                and response_body_create_order.get('order', {}).get('number') == response_body_getting_order.
                get('orders', [{}])[0].get('number'))

    @allure.title('Получаем заказ(ы) будучи неавторизованным пользователем')
    def test_getting_order_with_not_authorization(self):
        response_getting_order = requests.get(f'{GetUrl.URL}{Endpoint.GET_ORDER}')
        response_body_getting_order = response_getting_order.json()
        assert (response_getting_order.status_code == 401
                and response_body_getting_order.get('message') == 'You should be authorised')

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

