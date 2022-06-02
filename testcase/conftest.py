import pytest
from public.help import os
from debug import login_mobile, login_token, login_mobile_shipper
import requests
from dingding import send_ding


@pytest.fixture(scope="session", autouse=True)
def test_token_carrier():
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
    os.environ['token_carrier'] = res.json()["queryResult"]["entity"]


@pytest.fixture(scope="session", autouse=True)
def test_token_shipper():
    url = "http://shipper.hjzy56.com/api/oauth/login"
    data = {
        "mobile": login_mobile_shipper(),
        "password": "Qqw123456!",
        #    verifyCode: {}
        "grant_type": "password",
        "userType": "consign",
        "loginType": "password",
        "loginToken": login_token()
    }
    res = requests.post(url=url, json=data)
    os.environ['token_shipper'] = res.json()["queryResult"]["entity"]


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    send_ding.send_ding(terminalreporter)


if __name__ == '__main__':
    test_token_shipper()
