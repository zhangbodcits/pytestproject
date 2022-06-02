import hmac
import urllib.parse
import hashlib
import base64
import requests
import urllib3
import time

from public.log import logger
from public.read_data import ReadFileData

urllib3.disable_warnings()
read = ReadFileData()


def ding_sign():
    """
    发送钉钉消息加密
    :return:
    """
    timestamp = str(round(time.time() * 1000))
    secret = "SEC07e54da76a6e625967991b7d33eb422667abe5be81c9b94161b766773105a423"
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return timestamp, sign


def send_ding(terminalreporter):
    """
    发送钉钉消息
    :param plugin:
    :return:
    """
    headers = {"Content-Type": "application/json"}
    # 惠捷之星
    # access_token = "6e1710f12ac5d45314cf737ab789473f8954f17fd2fb5dd3e91bf1c8637d2a32"
    # 小云云
    access_token = "fe86177bed3761d722b2d9deefeb68577e820142474c970796ec576e0680605d"
    timestamp, sign = ding_sign()
    # 发送内容
    # summary = plugin.report.get("summary")
    # passed = summary.get("passed", 0)
    # failed = summary.get("failed", 0)
    # skipped = summary.get("skipped", 0)
    # total = summary.get("total", 0)
    # hlocal = "http://192.168.110.240:8080/job/project_testing/job/pytestproject01/allure/"
    # duration = plugin.report.get("duration", None)
    # start = time.localtime(plugin.report["created"] if plugin.report.get("created", None) else time.time())
    # start = time.strftime("%Y-%m-%d %H:%M:%S", start)
    total = terminalreporter._numcollected
    passed = len([i for i in terminalreporter.stats.get('passed', []) if i.when != 'teardown'])
    failed = len([i for i in terminalreporter.stats.get('failed', []) if i.when != 'teardown'])
    error = len([i for i in terminalreporter.stats.get('error', []) if i.when != 'teardown'])
    skipped = len([i for i in terminalreporter.stats.get('skipped', []) if i.when != 'teardown'])
    rate = passed / total * 100
    hlocal = "http://192.168.110.240:8080/job/project_testing/job/pytestproject01/allure/"
    # terminalreporter._sessionstarttime 会话开始时间
    duration = time.time() - terminalreporter._sessionstarttime
    body = {
        "msgtype": "text",
        "text": {
            "content": "接口测试报告 开始时间 {}，持续时长 {} 秒。\n 共 {} 条，通过 {} 条，失败 {} 条，跳过 {} 条,成功率{}%.\n 详情请前往：{}\n查看。".format(
                duration, duration, total, passed, failed, skipped, rate, hlocal)
        }
    }
    ding = read.get_system().get("ding", None)
    if ding == "true":
        res = requests.post(
            "https://oapi.dingtalk.com/robot/send?access_token={}&timestamp={}&sign={}".format(
                access_token, timestamp, sign), headers=headers, json=body, verify=False).json()
        if res["errcode"] == 0 and res["errmsg"] == "ok":
            logger.info("钉钉通知发送成功！info：{}".format(body["text"]["content"]))
        else:
            logger.error("钉钉通知发送失败！返回值：{}".format(res))
