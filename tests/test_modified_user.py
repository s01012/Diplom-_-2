import allure
import random
import requests
from utils.url import *
from utils.endpoint import *
from utils.test_data import *


class TestModifiedUser:
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

    @allure.title('Отправляем PATCH запрос на изменение email у авторизованного пользователя')
    def test_modified_user_email_with_authorization(self):
        gen_data = generator()
        payload = {
            'email': gen_data.get('email')
        }
        r = requests.patch(f'{GetUrl.URL}{Endpoint.MODIFY_USER_DATA}',
                           headers={'Authorization': f'{self.response_body.get("accessToken")}'}, data=payload)
        r_body = r.json()
        assert (r.status_code == 200 and r_body.get('user', {}).get('email') == payload.get('email')
                and r_body.get('success') == True)

    @allure.title('Отправляем PATCH запрос на изменение пароля у авторизованного пользователя')
    def test_modified_user_password_with_authorization(self):
        gen_data = generator()
        payload = {
            'password': gen_data.get('password')
        }
        r = requests.patch(f'{GetUrl.URL}{Endpoint.MODIFY_USER_DATA}',
                           headers={'Authorization': f'{self.response_body.get("accessToken")}'}, data=payload)
        r_body = r.json()
        assert r.status_code == 200 and r_body.get('success') == True

    @allure.title('Отправляем PATCH запрос на изменение имени у авторизованного пользователя')
    def test_modified_user_name_with_authorization(self):
        gen_data = generator()
        payload = {
            'name': gen_data.get('name')
        }
        r = requests.patch(f'{GetUrl.URL}{Endpoint.MODIFY_USER_DATA}',
                           headers={'Authorization': f'{self.response_body.get("accessToken")}'}, data=payload)
        r_body = r.json()
        assert (r.status_code == 200 and r_body.get('user', {}).get('name') == payload.get('name')
                and r_body.get('success') == True)

    @allure.title('Отправляем PATCH запрос на изменение email у неавторизованного пользователя')
    def test_modified_user_email_with_not_authorization(self):
        gen_data = generator()
        payload = {
            'email': gen_data.get('email')
        }
        r = requests.patch(f'{GetUrl.URL}{Endpoint.MODIFY_USER_DATA}', data=payload)
        r_body = r.json()
        assert (r.status_code == 401 and r_body.get('user', {}).get('email') != payload.get('email')
                and r_body.get('success') == False)

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
