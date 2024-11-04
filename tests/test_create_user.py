import allure
import requests
from utils.url import *
from utils.endpoint import *
from utils.test_data import *


class TestCreateUser:

    @allure.title('Отправляем POST запрос на создание пользователя с неиспользованными ранее данными')
    def test_create_user(self):
        gen_data = generator()
        payload = {
            'email': gen_data.get('email'),
            'password': gen_data.get('password'),
            'name': gen_data.get('name')
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_USER}', data=payload)
        response_body = response.json()
        assert response.status_code == 200 and response_body.get('success') == True and 'user' in response_body

    @allure.title('Отправляем POST запрос на создание пользователя с данными, которые уже есть в системе')
    def test_create_identical_user(self, registered_user):
        payload = {
            'email': registered_user['email'],
            'password': registered_user['password'],
            'name': registered_user['name']
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_USER}', data=payload)
        response_body = response.json()
        assert (response.status_code == 403 and response_body.get('success') == False
                and response_body.get('message')) == 'User already exists'

    @allure.title('Отправляем POST запрос на создание пользователя без пароля')
    def test_create_user_without_password(self, registered_user):
        payload = {
            'email': registered_user['email'],
            'password': '',
            'name': registered_user['name']
        }
        response = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_USER}', data=payload)
        response_body = response.json()
        assert (response.status_code == 403 and response_body.get('success') == False
                and response_body.get('message')) == 'Email, password and name are required fields'
