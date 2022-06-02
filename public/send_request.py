from public.common import recursion_handle, extract_variables, upload_file, parametrize_validate, validators_result, \
    not_empty
from public.read_data import ReadFileData
from base.bae_request import BaseRequest
from public.sign import decrypt
from jsonpath import jsonpath
from public.log import logger


class SendRequest:
    def __init__(self, test_data, extract):
        self.read = ReadFileData()
        self.send = BaseRequest(extract)
        self.test_data = test_data
        self.extract = extract
        self.extract.update(self.read.get_variable()) if not self.extract else self.extract

    def send_request(self):
        variable = self.test_data.variable if self.test_data.variable else {}
        # 加载测试数据中的固定变量
        self.extract.update(variable)
        # 非空判断， 请求方式转大写
        path = not_empty(self.test_data.path)
        method = not_empty(self.test_data.method).upper()
        headers = self.test_data.headers if self.test_data.headers else {}
        params = self.test_data.params if self.test_data.params else {}
        data = self.test_data.data if self.test_data.data else ""
        json = self.test_data.json if self.test_data.json else {}
        extract = self.test_data.extract if self.test_data.extract else {}
        parametrize = self.test_data.parametrize if self.test_data.parametrize else []
        validate = self.test_data.validate if self.test_data.validate else []
        upload = self.test_data.upload[0] if self.test_data.upload and self.test_data.upload[0] else []

        if upload:  # 上传文件
            file_path = self.test_data.file_path
            upload = upload_file(upload, file_path)
            headers["Content-Type"] = upload.content_type
        if parametrize:  # 参数化
            validate, parametrize = parametrize_validate(parametrize)
            if method == "GET":
                params = parametrize
            else:
                json = parametrize

        # 从全局变量中替换依赖值
        path = recursion_handle(path, self.extract)
        headers = recursion_handle(headers, self.extract)
        params = recursion_handle(params, self.extract)
        data = recursion_handle(data, self.extract)
        json = recursion_handle(json, self.extract)
        validate = recursion_handle(validate, self.extract)
        shipper = self.extract.get("shipper")
        if shipper == 1:
            url = self.read.get_host_shipper() + path if "http" not in path else path
        elif shipper == 2:
            url = self.read.get_host() + path if "http" not in path else path
        else:
            url = self.read.get_host() + path if "http" not in path else path
        result = self.send.request(url=url, method=method, headers=headers, params=params, data=data, json=json,
                               files=upload)
        if self.extract.get("sign"):
            sign_text = result.text
            sign_path = self.extract.get("sign_path")
            sign_data = jsonpath(result.text, sign_path)[0]
            sign_text = eval(str(sign_text).replace(sign_data, "$sign_data"))
            self.extract.update({"sign_data": decrypt(sign_data)})
            print(self.extract)
            print(sign_text)
            result.text = recursion_handle(sign_text, self.extract)
            validators_result(result, validate)  # 断言
            self.extract.update(extract_variables(result.response.json(), extract, self.extract))
        return result, self.extract
