import allure
import requests
from utils.url import *
from utils.endpoint import *
from utils.test_data import *


class TestCreateOrder:

    @allure.title('Отправляем POST запрос на создание заказа у авторизованного пользователя')
    def test_create_order_with_authorization(self, registered_user):
        r = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_ORDER}',
                           headers={'Authorization': f'{registered_user["access_token"]}'}, data=exact_ingredients)
        r_body = r.json()
        assert r.status_code == 200 and r_body.get('success') == True

    @allure.title('Отправляем POST запрос на создание заказа у неавторизованного пользователя')
    def test_create_order_with_not_authorization(self):
        r = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_ORDER}', data=exact_ingredients)
        r_body = r.json()
        assert r.status_code == 200 and r_body.get('success') == True

    @allure.title('Отправляем POST запрос на создание заказа БЕЗ ингредиентов, у авторизованного пользователя')
    def test_create_order_with_authorization_and_not_ingredient(self, registered_user):
        r = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_ORDER}',
                           headers={'Authorization': f'{registered_user["access_token"]}'})
        r_body = r.json()
        assert (r.status_code == 400 and r_body.get('success') == False
                and r_body.get('message') == 'Ingredient ids must be provided')

    @allure.title('Отправляем POST запрос на создание заказа c несуществующими ингредиентами в системе, '
                  'будучи авторизованным пользователем')
    def test_create_order_with_authorization_and_not_exact_ingredient(self, registered_user):
        r = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_ORDER}',
                           headers={'Authorization': f'{registered_user["access_token"]}'},
                          data=not_exact_ingredients)

        assert r.status_code == 500 and "text/html" in r.headers.get("Content-Type", "")
