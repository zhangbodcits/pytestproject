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

    def test_createorder_case(self, test_data):
        logger.info("*************** 开始执行用例 ***************")

        report_step_setting(test_data.case_step_1)
        # 登录接口
        result, self.extract = SendRequest(test_data.case_step_1, self.extract).send_request()

        # 报告展示的测试步骤
        report_step_setting(test_data.case_step_2)
        # 登录接口
        result, self.extract = SendRequest(test_data.case_step_2, self.extract).send_request()

        report_step_setting(test_data.case_step_3)
        # 登录接口
        result, self.extract = SendRequest(test_data.case_step_3, self.extract).send_request()
        report_step_setting(test_data.case_step_4)
        # 登录接口
        result, self.extract = SendRequest(test_data.case_step_4, self.extract).send_request()
        # 报告上展示的测试标题等
        report_setting(test_data.case_step_1)
        logger.info("*************** 结束执行用例 ***************\n")

    @pytest.mark.skip("测试")
    def test_sign_case(self, test_data):
        logger.info("*************** 开始执行用例 ***************")
        # 报告展示的测试步骤
        report_step_setting(test_data)
        # 登录接口
        result, self.extract = SendRequest(test_data, self.extract).send_request()

        # 报告上展示的测试标题等
        report_setting(test_data)
        logger.info("*************** 结束执行用例 ***************\n")

        # @pytest.mark.parametrize("data", test_params["test_createorder_case"].parametrize)
        # def test_createorder_case(self, data, test_data):
        #     logger.info("*************** 开始执行用例 ***************")
        #     # 获取执行用例函数名
        #     name = fun_name()
        #     # 报告展示的测试步骤
        #     report_step_setting(test_params[name])
        #
        #     # 重置测试数据
        #     test_params[name].parametrize = data
        #     # 发送接口请求，断言，返回提取变量字典
        #     result, self.extract = SendRequest(test_params[name], self.extract).send_request()
        #     # 报告展示的测试步骤
        #     report_step_setting(test_params[name])
        #
        #     # 重置测试数据
        #     test_params[name].parametrize = data
        #     # 发送接口请求，断言，返回提取变量字典
        #     result, self.extract = SendRequest(test_params[name], self.extract).send_request()
        #
        #     # 报告上展示的测试标题等
        #     report_setting(test_params[name])
        #     logger.info("*************** 结束执行用例 ***************\n")


if __name__ == '__main__':
    pytest.main(
        ["-q", "-s", "test_homepage_case.py", "-W", "ignore:Module already imported:pytest.PytestWarning"])
