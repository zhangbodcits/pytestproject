import pytest
from public.send_request import SendRequest
from public.log import logger
from public.sql_to_data import SqlToData
from public.help import get_data_path, os, fun_name, report_setting, report_step_setting, allure
import Crypto
from public.read_data import ReadFileData
from public.help import get_extract_path

data_path = get_data_path(os.path.dirname(__file__))
test_params = SqlToData().yaml_db_query(data_path)


@allure.severity(allure.severity_level.TRIVIAL)
@allure.epic(test_params.get("epic"))
@allure.feature(test_params.get("feature"))
class TestSignCase:
    def setup_class(self):
        self.extract = {}

    # 登录接口
    def test_tuo_login_case(self, test_data):
        logger.info("*************** 开始执行用例 ***************")
        # 报告展示的测试步骤
        report_step_setting(test_data)
        # 登录接口
        result, self.extract = SendRequest(test_data, self.extract).send_request()
        # 报告上展示的测试标题等
        report_setting(test_data)
        logger.info("*************** 结束执行用例 ***************\n")


if __name__ == '__main__':
    pytest.main(
        ["-q", "-s", "test_homepage_case.py", "-W", "ignore:Module already imported:pytest.PytestWarning"])
