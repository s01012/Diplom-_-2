import pytest
import requests
from utils.url import GetUrl
from utils.endpoint import Endpoint
from utils.helpers import generate_random_email, generate_random_password, generate_random_name

@pytest.fixture(scope='class')
def registered_user():
    user_info = {
        'email': generate_random_email(),
        'password': generate_random_password(),
        'name': generate_random_name()
    }
    response_create = requests.post(f'{GetUrl.URL}{Endpoint.CREATE_USER}', data=user_info)
    user_info['access_token'] = response_create.json().get("accessToken")

    yield user_info

    response_login = requests.post(f'{GetUrl.URL}{Endpoint.LOGIN_USER}', data=user_info)
    response_body = response_login.json()
    requests.delete(f'{GetUrl.URL}{Endpoint.DELETE_USER}',
                    headers={'Authorization': f'{response_body.get("accessToken")}'})