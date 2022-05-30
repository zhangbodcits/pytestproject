import os
import pytest
from pytest_jsonreport.plugin import JSONReport


if __name__ == '__main__':
    # plugin = JSONReport()
    # pytest.main(plugins=[plugin])
    # send_ding.send_ding(plugin)
    pytest.main()
    os.system("allure generate ./report --clean allure-reports -o ./report/html")
    # print(111111)
