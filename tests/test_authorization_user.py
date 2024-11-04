import allure
import requests
from utils.url import *
from utils.endpoint import *
from utils.test_data import *


class TestAuthorizationUser:

    @allure.title('Отправляем POST запрос для авторизации ранее зарегистрированного пользователя')
    def test_authorization_user(self, registered_user):
        payload = {
            'email': registered_user['email'],
            'password': registered_user['password']
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
