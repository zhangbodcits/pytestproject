from Crypto.Cipher import AES
import base64
import binascii


# 数据类
class MData():
    def __init__(self, data=b"", characterSet='utf-8'):
        # data肯定为bytes
        self.data = data
        self.characterSet = characterSet

    def saveData(self, FileName):
        with open(FileName, 'wb') as f:
            f.write(self.data)

    def fromString(self, data):
        self.data = data.encode(self.characterSet)
        return self.data

    def fromBase64(self, data):
        self.data = base64.b64decode(data.encode(self.characterSet))
        return self.data

    def fromHexStr(self, data):
        self.data = binascii.a2b_hex(data)
        return self.data

    def toString(self):
        return self.data.decode(self.characterSet)

    def toBase64(self):
        return base64.b64encode(self.data).decode()

    def toHexStr(self):
        return binascii.b2a_hex(self.data).decode()

    def toBytes(self):
        return self.data

    def __str__(self):
        try:
            return self.toString()
        except Exception:
            return self.toBase64()


### 封装类
class AEScryptor():
    def __init__(self, key, mode, iv='', paddingMode="NoPadding", characterSet="utf-8"):
        '''
        构建一个AES对象
        key: 秘钥，字节型数据
        mode: 使用模式，只提供两种，AES.MODE_CBC, AES.MODE_ECB
        iv： iv偏移量，字节型数据
        paddingMode: 填充模式，默认为NoPadding, 可选NoPadding，ZeroPadding，PKCS5Padding，PKCS7Padding
        characterSet: 字符集编码
        '''
        self.key = key
        self.mode = mode
        self.iv = iv
        self.characterSet = characterSet
        self.paddingMode = paddingMode
        self.data = ""

    def __ZeroPadding(self, data):
        data += b'\x00'
        while len(data) % 16 != 0:
            data += b'\x00'
        return data

    def __StripZeroPadding(self, data):
        data = data[:-1]
        while len(data) % 16 != 0:
            data = data.rstrip(b'\x00')
            if data[-1] != b"\x00":
                break
        return data

    def __PKCS5_7Padding(self, data):
        needSize = 16 - len(data) % 16
        if needSize == 0:
            needSize = 16
        return data + needSize.to_bytes(1, 'little') * needSize

    def __StripPKCS5_7Padding(self, data):
        paddingSize = data[-1]
        return data.rstrip(paddingSize.to_bytes(1, 'little'))

    def __paddingData(self, data):
        if self.paddingMode == "NoPadding":
            if len(data) % 16 == 0:
                return data
            else:
                return self.__ZeroPadding(data)
        elif self.paddingMode == "ZeroPadding":
            return self.__ZeroPadding(data)
        elif self.paddingMode == "PKCS5Padding" or self.paddingMode == "PKCS7Padding":
            return self.__PKCS5_7Padding(data)
        else:
            print("不支持Padding")

    def __stripPaddingData(self, data):
        if self.paddingMode == "NoPadding":
            return self.__StripZeroPadding(data)
        elif self.paddingMode == "ZeroPadding":
            return self.__StripZeroPadding(data)

        elif self.paddingMode == "PKCS5Padding" or self.paddingMode == "PKCS7Padding":
            return self.__StripPKCS5_7Padding(data)
        else:
            print("不支持Padding")

    def setCharacterSet(self, characterSet):
        '''
        设置字符集编码
        characterSet: 字符集编码
        '''
        self.characterSet = characterSet

    def setPaddingMode(self, mode):
        '''
        设置填充模式
        mode: 可选NoPadding，ZeroPadding，PKCS5Padding，PKCS7Padding
        '''
        self.paddingMode = mode

    def decryptFromBase64(self, entext):
        '''
        从base64编码字符串编码进行AES解密
        entext: 数据类型str
        '''
        mData = MData(characterSet=self.characterSet)
        self.data = mData.fromBase64(entext)
        return self.__decrypt()

    def decryptFromHexStr(self, entext):
        '''
        从hexstr编码字符串编码进行AES解密
        entext: 数据类型str
        '''
        mData = MData(characterSet=self.characterSet)
        self.data = mData.fromHexStr(entext)
        return self.__decrypt()

    def decryptFromString(self, entext):
        '''
        从字符串进行AES解密
        entext: 数据类型str
        '''
        mData = MData(characterSet=self.characterSet)
        self.data = mData.fromString(entext)
        return self.__decrypt()

    def decryptFromBytes(self, entext):
        '''
        从二进制进行AES解密
        entext: 数据类型bytes
        '''
        self.data = entext
        return self.__decrypt()

    def encryptFromString(self, data):
        '''
        对字符串进行AES加密
        data: 待加密字符串，数据类型为str
        '''
        self.data = data.encode(self.characterSet)
        return self.__encrypt()

    def __encrypt(self):
        if self.mode == AES.MODE_CBC:
            aes = AES.new(self.key, self.mode, self.iv)
        elif self.mode == AES.MODE_ECB:
            aes = AES.new(self.key, self.mode)
        else:
            print("不支持这种模式")
            return

        data = self.__paddingData(self.data)
        enData = aes.encrypt(data)
        return MData(enData)

    def __decrypt(self):
        if self.mode == AES.MODE_CBC:
            aes = AES.new(self.key, self.mode, self.iv)
        elif self.mode == AES.MODE_ECB:
            aes = AES.new(self.key, self.mode)
        else:
            print("不支持这种模式")
            return
        data = aes.decrypt(self.data)
        mData = MData(self.__stripPaddingData(data), characterSet=self.characterSet)
        return mData


if __name__ == '__main__':
    key = b"nsz3*H&I@xINg/tH"
    iv = b"0000000000000000"
    aes = AEScryptor(key, AES.MODE_ECB, iv, paddingMode="PKCS7Padding", characterSet='utf-8')

    data = "17666666666"
    rData = aes.encryptFromString(data)
    print("密文：", rData.toHexStr())
    rData = aes.decryptFromHexStr("75684346929bede97f82c8818a987ad4a47dfff46727d7650e73b51186f73d3602a8bac444b8e5c8e7707425c03c76fd43bf7cb8d995b599918d9d03dca9f16d556f6551b25afe7b55ed3b91099d2ac264f96c6eeed83b9911d066ca03a0099cb2f36b3daae2790b62194884ca71551b00dc5169e6996e9547cfc622b7e7fda50c6ee7350f73a8b88e5850ec7b56ad4218830c900d354c76d3db142be9311efbc7f315d1f748915ae83bd53980ba57d7f0a58119edcb14a87f06c57df71bb0db38de98bdb4e21dd9c69cf2c42fa35338b3854e713eae1b8a9796aa0150182d9daf67c9c491989618cf67760b8daf9daba5dba980c82e716984814dccd6ab9710cbbfca7c42eebba5bde9eccaadffac1edc9b4160c298e047f089babe450d39b9396501926ec3bbd62b16e3956324c962760ae2404808d7f66fffb080f96bd81618288664ea3e559b6c29d0c03863d801c8db8ca77562bf6d0c6c0fc89570616fba5649b14e08682381d2885e0e14a4ee3a8407ee13ba5dc7ca8aac59811b32fdee3ffe0331afa1407145f18251d35e75f408796d8b1473afc91ea5f2dfdefa3a78615dd80d99523195b3f10eedfaf857305f8c606fb14fe3db0555bdf7ce32ed")
    print("明文：", rData)

