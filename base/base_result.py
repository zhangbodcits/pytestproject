class BaseResult:

    def __init__(self):
        self.success = False
        self.status_code = 200
        self.error = ""
        self.response = ""
        self.message = ""
        self.code = 0
        self.text = {}

    def default_assert(self, response):
        """
        默认断言
        :param response:
        :return:
        """
        self.response = response
        self.status_code = response.status_code
        if response.status_code == 200:
            self.success = True
        else:
            self.error = "接口返回码是 {}，返回信息：{}".format(self.status_code, response.text)
        try:
            self.text = self.response.json()
        except Exception as error:
            self.text = self.response.content
        return self
