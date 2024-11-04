import allure
import requests
from utils.url import *
from utils.endpoint import *
from utils.test_data import *


class TestGettingOrder:

    @allure.title('Получаем заказ(ы) авторизованного пользователя')
    def test_getting_order_with_authorization(self, registered_user):
        response_create_order = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_ORDER}',
                           headers={'Authorization': f'{registered_user["access_token"]}'}, data=exact_ingredients)
        response_body_create_order = response_create_order.json()
        response_getting_order = requests.get(f'{GetUrl.URL}{Endpoint.GET_ORDER}',
                           headers={'Authorization': f'{registered_user["access_token"]}'})
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
