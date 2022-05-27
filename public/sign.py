from Crypto.Cipher import AES
import binascii
import re

from public.log import logger

def decrypt(data) -> str:
    """
    AES 解密
    :param data: 要解密的数据
    :return:
    """
    key = b"nsz3*H&I@xINg/tH"
    data = binascii.a2b_hex(data)
    aes = AES.new(key, AES.MODE_ECB)
    data = aes.decrypt(data)
    data = data.decode('utf-8').strip('\t').strip("\u0007")
    patt = "([\\[{].+[\\]}])"
    data = re.findall(patt, data)[0]
    logger.info("解密后的数据：{}".format(data))
    return data


def add_to_16(text):
    if len(text.encode('utf-8')) % 16:
        add = 16 - (len(text.encode('utf-8')) % 16)
    else:
        add = 0
    text = text + ('\0' * add)
    return text.encode('utf-8')


def encrypt(data) -> str:
    """
    AES 解密
    :param data: 要解密的数据
    :return:
    """
    key = b"nsz3*H&I@xINg/tH"
    aes = AES.new(key, AES.MODE_ECB)
    data = aes.encrypt(add_to_16(data))
    return binascii.b2a_hex(data).decode()


if __name__ == '__main__':
    data = decrypt("1528585841738743809")
    print(data)
