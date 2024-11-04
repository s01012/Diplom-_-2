import allure
import requests
from utils.url import *
from utils.endpoint import *
from utils.test_data import *


class TestModifiedUser:

    @allure.title('Отправляем PATCH запрос на изменение email у авторизованного пользователя')
    def test_modified_user_email_with_authorization(self, registered_user):
        gen_data = generator()
        payload = {
            'email': gen_data.get('email')
        }
        r = requests.patch(f'{GetUrl.URL}{Endpoint.MODIFY_USER_DATA}',
                           headers={'Authorization': f'{registered_user["access_token"]}'}, data=payload)
        r_body = r.json()
        assert (r.status_code == 200 and r_body.get('user', {}).get('email') == payload.get('email')
                and r_body.get('success') == True)

    @allure.title('Отправляем PATCH запрос на изменение пароля у авторизованного пользователя')
    def test_modified_user_password_with_authorization(self, registered_user):
        gen_data = generator()
        payload = {
            'password': gen_data.get('password')
        }
        r = requests.patch(f'{GetUrl.URL}{Endpoint.MODIFY_USER_DATA}',
                           headers={'Authorization': f'{registered_user["access_token"]}'}, data=payload)
        r_body = r.json()
        assert r.status_code == 200 and r_body.get('success') == True

    @allure.title('Отправляем PATCH запрос на изменение имени у авторизованного пользователя')
    def test_modified_user_name_with_authorization(self, registered_user):
        gen_data = generator()
        payload = {
            'name': gen_data.get('name')
        }
        r = requests.patch(f'{GetUrl.URL}{Endpoint.MODIFY_USER_DATA}',
                           headers={'Authorization': f'{registered_user["access_token"]}'}, data=payload)
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
