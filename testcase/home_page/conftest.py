import pytest
from public.sql_to_data import SqlToData
from public.help import get_data_path, os

data_path = get_data_path(os.path.dirname(__file__))


@pytest.fixture(scope="function")
def test_data(request):
    to_data = SqlToData()
    testcase_name = request.function.__name__
    data = to_data.yaml_db_query(data_path)
    return data.get(testcase_name)
