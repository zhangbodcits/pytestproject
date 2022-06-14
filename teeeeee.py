# -*- coding: utf-8 -*-            
# @Time : 2022/6/2 16:32
# @Author:mr.Zhang
# @FileName: teeeeee.py
# @Software: PyCharm
import requests
from tools.encryptDate import AEScryptor
from Crypto.Cipher import AES
from public.sign import decrypt
import json
from jsonpath import jsonpath

headers = {
    "jtiToken": "1533620976391774209",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
}
res = requests.get(
    # url="http://operation.hjzy56.com/gateway/api/operationManagement/carrier/driver/list/?page=1&pageSize=100",
    # url="http://operation.hjzy56.com/gateway/api/operationManagement/finance/wallet/list?page=1&pageSize=10000&customuserNameuserPhone=userName&syncDriverStatus=2&userName=&uu=52741db4-290d-82af-8d1c-62ec9ae7cd4f",
    url="http://operation.hjzy56.com/gateway/api/operationManagement/finance/wallet/list?page=1&pageSize=1000&customuserNameuserPhone=userName&yopOpenStatus=1&userName=&uu=cba34864-a30f-bbba-9482-16c58ac7eb6e",
    headers=headers)
data = res.json()
# print(data, 11111111111111111111111)
key = b"nsz3*H&I@xINg/tH"
iv = b"0000000000000000"
# aes = AEScryptor(key, AES.MODE_ECB, iv, paddingMode="PKCS7Padding", characterSet='utf-8')
# rData = aes.decryptFromHexStr(dict)
str_data = decrypt(data["map"]['queryResult'])
# data["map"]['queryResult'] = json.loads(str_data)
# patt = "$.map.queryResult.list[*].driverName"
# name = jsonpath(data, patt)
# print(name)
data = json.loads(str_data)["list"]
print(data)
list1 = []
for item in data:
    # if item['driverName'] is None:
    #     item['driverName'] = "测试"
    # else:
    #     print(item['driverName'], item["telephone"])
    try:
        list1.append(item['userName'])
    except:
        item['userName'] = "测试"
print(list1)