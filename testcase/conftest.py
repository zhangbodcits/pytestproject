import pytest
from public.help import os
from debug import login_mobile, login_token
import requests


@pytest.fixture(scope="session", autouse=True)
def test_token():
    url = "http://operation.hjzy56.com/gateway/api/oauth/login"
    data = {
        "mobile": login_mobile(),
        "password": "zb123456.",
        #    verifyCode: {}
        "grant_type": "password",
        "userType": "operation",
        "loginType": "password",
        "loginToken": login_token()
    }
    res = requests.post(url=url, json=data)
    os.environ['token'] = res.json()["queryResult"]["entity"]


if __name__ == '__main__':
    test_token()
