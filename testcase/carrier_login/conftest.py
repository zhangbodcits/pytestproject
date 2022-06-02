import pytest
from public.sql_to_data import SqlToData, ReadFileData
from public.help import get_data_path, os
from debug import login_mobile, login_token
import requests

data_path = get_data_path(os.path.dirname(__file__))


@pytest.fixture(scope="function")
def test_data(request):
    to_data = SqlToData()
    testcase_name = request.function.__name__
    data = to_data.yaml_db_query(data_path)
    # extract_data = ReadFileData().load_yaml(BASE_PATH)
    # print(extract_data)
    # yield data.get(testcase_name), extract_data
    return data.get(testcase_name)
    # ReadFileData().clean_yaml(BASE_PATH)


# @pytest.fixture(scope="session", autouse=True)
# def test_token():
#     url = "http://operation.hjzy56.com/gateway/api/oauth/login"
#     data = {
#         "mobile": login_mobile(),
#         "password": "zb123456.",
#         #    verifyCode: {}
#         "grant_type": "password",
#         "userType": "operation",
#         "loginType": "password",
#         "loginToken": login_token()
#     }
#     res = requests.post(url=url, json=data)
#     os.environ['token'] = res.json()["queryResult"]["entity"]


