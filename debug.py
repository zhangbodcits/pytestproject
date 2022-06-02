import io
import csv
import os.path

from public.help import check, CASE_PATH
from public import exceptions
from tools.encryptDate import AEScryptor
from Crypto.Cipher import AES


def username():
    return 'lixiaofeng'


def password():
    return "123456"


def load_csv(file_path: str) -> list:
    """
    读取参数化csv文件数据
    :param file_path: 文件路径
    :return:
    """
    file_path = os.path.join(CASE_PATH, file_path)
    parametrize_list = list()
    # logger.info(f"加载 {file_path} 文件......")
    with io.open(check(file_path), encoding='gbk') as f:
        reader = csv.DictReader(f)
        for value in reader:
            parametrize = list()
            # del value["case_name"]
            validate_list = list()
            params_list = list()
            try:
                key = ",".join(value.keys()).strip()
                key_list = key.split(",,")
            except Exception as error:
                raise exceptions.CSVFormatError("csv文件数据格式异常！{error}".format(error=error))
            if len(key_list) == 1:
                params_list.append(value)
                parametrize.append(params_list)
            elif len(key_list) == 2:
                params_key_list = key_list[0]
                validate_key_list = key_list[1]
                for k, v in value.items():
                    if k and k in params_key_list:
                        parametrize.append({k: v})
                    elif k and k in validate_key_list:
                        if v:
                            validate_value = eval(v)
                            validate_value.update({"check": k})
                            validate_list.append([validate_value])
                parametrize.append({"validate": validate_list})
            else:
                raise exceptions.CSVFormatError("csv文件数据格式异常！")
            parametrize_list.append(parametrize)
    # logger.info(f"读到数据 ==>>  {parametrize_list} ")
    return parametrize_list


def rand_str():
    import hashlib
    import datetime
    now = datetime.datetime.now().strftime('%Y%m%d')
    h = hashlib.md5()
    h.update(now.encode(encoding='utf-8'))
    return h.hexdigest()


def rand_str1():
    key = b"nsz3*H&I@xINg/tH"
    iv = b"0000000000000000"
    aes = AEScryptor(key, AES.MODE_ECB, iv, paddingMode="PKCS7Padding", characterSet='utf-8')

    data = "19135221679"
    rData = aes.encryptFromString(data)
    print("密文：", rData.toBase64())
    rData = aes.decryptFromHexStr("2a5c22b518c0db7c07fc39f07aff4b7a40d357504a51a631c3c3e1ce842ec489")
    print("明文：", rData)
    return rData.toBase64()


def login_token():
    import hashlib
    import time
    import datetime
    now = datetime.datetime.now().strftime('%Y%m%d')
    h = hashlib.md5()
    h.update(now.encode(encoding='utf-8'))
    return h.hexdigest()


def login_mobile():
    from Crypto.Cipher import AES
    from tools.encryptDate import AEScryptor
    key = b"nsz3*H&I@xINg/tH"
    iv = b"0000000000000000"
    aes = AEScryptor(key, AES.MODE_ECB, iv, paddingMode="PKCS7Padding", characterSet='utf-8')
    return aes.encryptFromString("19135221679").toHexStr()


def login_mobile_shipper():
    from Crypto.Cipher import AES
    from tools.encryptDate import AEScryptor
    key = b"nsz3*H&I@xINg/tH"
    iv = b"0000000000000000"
    aes = AEScryptor(key, AES.MODE_ECB, iv, paddingMode="PKCS7Padding", characterSet='utf-8')
    return aes.encryptFromString("18234175957").toHexStr()


def token_carrier():
    return os.getenv("token_carrier")


def token_shipper():
    return os.getenv("token_shipper")

def get_userAgent():
    userAgent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
    return userAgent


if __name__ == '__main__':
    print(token_carrier())
    print(token_shipper())
    print(login_mobile_shipper())
