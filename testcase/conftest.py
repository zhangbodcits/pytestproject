import pytest
from public.help import os
from debug import login_mobile, login_token
import requests
from dingding import send_ding


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


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    send_ding.send_ding(terminalreporter)
