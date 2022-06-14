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

    data = "19135221679"
    rData = aes.encryptFromString(data)
    print("密文：", rData.toHexStr())
    rData = aes.decryptFromHexStr("75684346929bede97f82c8818a987ad4a47dfff46727d7650e73b51186f73d3602a8bac444b8e5c8e7707425c03c76fd1238fc8af2708d244ec06f4c9e0d42529ad3457b5da648ccfb140f489ddc2fb5f8dca2d160b265b13920940e68e8e02e4e84ceb5854bdc926376f8af0a442864e630326c9b4d4f0be43336aa5b9791a737c43d3d26aff2a9dce31e6f6adab1f026adb3e11cb8b8ff2fe0b65164d7135e76488cc66c05c5f26d5aa24aecca5063fb83081da55e06500efb5adf66197b388d6617dc58eae0eb3af3fca9d008ce6da508af96eaa0ed8207232b650393cdd09233841791358fc7fd6f9e7942667c0f2f05c0e66db3dfa1272e11e610676895855fcd62799251d7f3f302de3cfad79b825f1f445fcd90f1ab18644ec3a62495cbde1e3b02b9ecd3c29f3b237e176e1bb5a69359ca01ea3666569b30236cb39b999252ec1a7dc4be9eee09bfbcb508f8455a8fbd225004dc1a407ee307534473aa78d38279043fb1ce9f284ef721d8dd15796e6c18463382212882e94ab18fabffd51960720bbb79dd0273171665dcaef369a5f4ddb8b259bf2a55ad4ecbef421c57be0de60d24ff14dcb16fb91ca8a7be42fc0a5c53b487bb113250700268d6b740831f4128decfac89b90733b801201136035ce8516afc31fa6eda3c519dbed8a4ef70b7e3fa4a4dadc88df75d24366c362327003de64d06b698308bac871e21d481c6c1a93415ecf29b3adbd017d9a12571ed111808e86c109fc755a84626e65993571c54ede24ba14e37954497a7b470f8fdfdb73adb7caa34eb6a7f21a003c1f31688dd1d4d1681f35801b4b2e2ae8a5a9957d1528202df6154f5a59f083dddc05578f90bb47bd55a43bcf5fb6c93e353a995f53695833da1f880d7d3c10b56464e8052f8ac7306de738195c250415a7154669d508602e4c111589e0957f9ccf15b94e927b0ed838ac0c5ea0bfa632356a21ebac03a7e977bb25975e434558162bfbd9c7ad640eee15b409da866fe40c4d21696827bcfb667b45179412a95622496e951075d7f5b4e82060dc58e61e39de5c6ce0283d36d5cd3bef6e988f6252deaebfc7284b213468631e4671612154b7b44788a3694432d3e4751744143c66211240192b74a172739d9104d0b113e5fc14cf1911634e6879ad1dcd2470f22b6ba09acffc89ab4967262aa00ed6f7b2081a3994b76034e7c5ff3e88f5e2df469bdc0d335d25f19ab72e00b22b7556e664da45c19fe7b7f87b5e63bf84dac1b2a9f728bd9c1e5093334139b8382455a8fbd225004dc1a407ee3075344731eee337753e9113d10c8a16265f9e8a12dd72ca549e2300548267ee8ab492cf7299207554e793597d71527abd22d2c584dd2853df30f40303561325776a8dba0a5960572ad037ee125597d08b527f648851a632f7da9453fd78ca2811daf7433c603d15f1da8160b92a3a01c9f805ca5bf11d31ab069110d1ff91d08c6ba38819d4e688a44a89a67a0cfd4832823ae5e5fde6448220b047132ecb0078f8c1992136cd1ced2f4717a6c5f562a8293402bda281649c7bc64948ab6ca19478bd26a0e4af49a3cc4d2eaafaabd4213c53c2f37c43d3d26aff2a9dce31e6f6adab1f0a65a368059123a0b1f12b51603afaeed05cc14405af18750047f166967d9c558adc037d3653282cbc20eed606ac8f2fe083ea3ae37a8c0180c71b541d2a5abc4513ae71d612876d473364af56d2e1ad0a2c2416ec5077ef39ff61dfc8e781bea59ee198135f83767b0ec6bfb0903d87b9c130d4ed9dc8627c83542caa2e6863e88552ff1c38733456d6f26f5261cee2585623423d360be399989d7c6e00f1c9dcb155c4a4df15e589884b17212c2caf1b68a88e81b13bb6382c18c4632fe9892849012d6b0868875ba2a5fb4e652a1cbd158492769cf27401751d428266f1f81faa86f1080b67eb797c846431e266bb5237a281f78fe2e844882754776aec006e3850669aa3e72f8dad13e2882faf21f51be04517a3cfbdf6a7639b253cf7efc7337616943dbd7782a57336f18150cab96b04bef308752fe8d7fe201e0bb3b7b241bcdfb7ea7658386f8df3f31baa84f799a65bc03b11f3a111a906a86f691515ff7181fd623664dbc9956730a01ba2246f071fbbde24886ef89303f83bf91b697deac91cd821bc1fc843fb5229240f4364c35295058f16483e3ffbd0297b53464e218d53e8451c9aaf2f1c77d4a89bc87fd6047bb6dc2c507daa87dac2c726ce977ade0b029697c6939cbd777d209843766a9f473ca7ffd7987b1f46728bb44069ca433250d633bcf8dfec4192c4a961513b24543581bb9d3750f38df044301f22d99e6bd26bacc46878128314854c04298da5651bfbde57b7478a801675dd1d72b937918542b1454384d3015b79bc28f53a65778c27fd2b0bc3f39c6d4f6739ff4736c3763baef7ce1d4fcf04c1897ad157b6842decc80db2cb2cc95f98468ebdaf942a33929791cc5e8a5a292dc5a2a8efae1b4e6b443f5f173e470cc13cff60287bd1edd316aefb763817980ca9772614ab72579adb794319dce3be3c85b2ce269b986b2f2326f8a78f8113b227f5456a1b57a2ff807284d41434948c098180f44e4224d641edc635bb6d79da8fd9584cc07c3148af6213d55274ed002ee8fd3668692f4d1e66861ca3ad9c2fb270544df533e445c5f8dfff28ca774d39fe705de2e0f1ca6e9206080bda6d0018529da072f1adfd9094e8f17e949efb1ac06df6131f8a4cfc731d8ac7883fff006368a146e1e1b3f1a5666ca89da4f101fa28c13c84638b1583fd3aa2b1ec42664ca328616af90fd8f647f7b121c6f4cc61c9f7198578f68c82a842fc9cf74e95d67abe566f249205524bef03bd3373084ae13c61a20eec6a1fe29e97cb49c421331e6e4a82906a14f9082461f94a66b8dd34a79eee9e86aba118806227c95b7975beb7205152d518ae35414d88eb87929b09c86748062c0d9fd1a214f6f66b5d9caf04993563e37094cfcdcc2ffc06abc346fbe1590d486d17968109f5c7b6311634d8c47a56da77e0d9b8dc56cd7ab856f80cebfcfc7ba201d40149a713589684d9ca09701d1b7ed9fd6f97f480fa6a5443788053a39c60a2d47630660939c787fa5ad39443b414468b8b0d6b426038bed498093b594315db85e54dc5406e55378cdec9b42888d0c2d27911c1964e77c1185b46cbbc36facb955751f1c474606e3f23d554163b307418968c48ddd84c6d574cc3874bd4fa0224d84634fda9d5c13aa39201597d60f60e809ffa3719e6905a5393d38c44a9d411437ec069de593f9c81b8664888a0c535135a4fdd0d0e532483f5e49b5266fa460ab35887e626dd64c315c4bbf65038d220b620256fe62ab2cb605e5ad62716c310d608e1caf229139ccf3c5bc8aa5920ac45bca60a8774a276e72f144629737794611766e8d9f2ef63b933bd4e4717b01491556e5b8b6f31a714c9ab2aa9857c08a80a3e3a9a7334065e06980b2a7141468be40efb1da59ee8386c8be6866a600223e8c88c632c16a381824135f6eb37fe1eb028fecc1a319d44d4842709027cf11125f7328003a47a94f31b9f2368127932223fd64ff02b26f59b02a7ad1c7e59b2e6f2567e7f70787c1a994f465dd216b40fec80cf5dd5b89a33495b0fb988ead012e03d08d8d336452a9211ede75dc343b1469a0d8a988dc42277ce6ca4075aac84e17efd0c670bbfb2366b97ca93bde99b64c50bf95dbd0b5b2727b3444b7ee33765184a4371f76a50fb24f817c8c20a682e215c99b8dacd79965056c297da0f83c000fcde3e622ae901638d3551a1fe3a990a42a920e49a6cb949f0e33c857949e7dd15260bf470f9dbe9085f38103266e332479d58a721f735b635ddaa4653b3f1312e23c6c0bedb1afe6d9900720f9ef16e8aae156bff27c0ba16b74bbc1dd787883b8736ac8bbe0d0e2e08ae23ad12550b7d7690799f04e72b2deeeca3fd76d16fe4fb24b1bbf78a8322907eb5b0192519e222e0db9f7b36be654b5ea93804069e028cedd89243b03ae3bb3f3ea38f21aa811423aeb30f5e6ef1962518b06c7de3cef28c4e1afaecbcc1751266de1140f21a6d0d3285df77a3fae8222c47ea7427e0a20bc07be2c69c6872440d60061d856af7276e0b0bef06559fb785605e4d7f6ba9e8b2723c9f3f27ae7fa32a3c3ecd0bf32675bf9858e35a3c3c3caae0128b1bbb8d332b357ae5ff0d2eba270a21701a60dc3edbbdc9637bd8caa69dcd9500628acc73bf9ab10c7a645309fef332bfc386520122438b4bfc310108900f947e26d192e645a6af65afa566ec4ceb955b8df7d57ed54e230136ba54301e4a88dc769c3fbb211ad75f4e580131911c7238cfd3fb8584e7de4a3b3a9774363ee003cbb27e6ccab1456a9b049762cb9159eaa42039def14e535d7430746447c5a154e446f634ab2628a38a111b8cfc6aa30d05a42417797145bb296c9c203193b3d86eac74e656c0743090d53d6b49a95946fbe4af92ba3aa27d0fa07788682ddee01037e1903dc7b9b98c7a36aa139441fb12c0d70a09fb98e024cfb8507f165131d8a8f2cc53074edfb0d5c3f19ae91cdd2462f25389389a8594bb57874f7f462d48d18d9748716f6e14256bb3a0caa010a7792feba4347e51dfae5c98af711c02050e39a6afae9700ebb7e70f1e9a72ba950459e7c7a28542aaf731747442369bba2197e04cf2a61f6d9f1e4a1b890af8c943dde284222d5de3042f97103f483019590ce3df449103a3f30f22b69f4df73290d96879fb40957f7ecd25046a214dbaf379f4be8b9490676a138281a91d7eaaf28fcace5c39800b23d1445bb2d6ba0b080f24764c42653c25ba3b26a0e57c2f4363169765190e83ba8df3ec747aabb864f0c53fbc6a5767e093b22302026c8d5cf3463f7f0f8d71821af1083f794a7602b529a9274dc164f2480fe362ca7a7de032b86aabf8860a18bcb0e455f4cc7aeca2a103d143d1d7493dea44417001b86fb85ec555e827a226d71c8f3800ca41b9f9a6c3147844ec64b0f2a77ba887ebf0e71c9478ef7c72aa56badd6e48f79ccf8eb2e62461f6eddea6d3daa554c4deb5a51b3518f2ccd2613709b4ec3c553fc1a42aff887051c21181cf1ced4463a2b09f192e7d96d3a97f64273b394f4f30bd720e240ea8331ebb6df48857e4a5f1ba5b4ac3c4b1d3e4d45fad65b7b4b4889f32ae4aa4570573bc4b6e1744bf6599986db16daaa396b77dd2e3422e2c3a51f496bfea6f30751b743500119c6510c51e18cd2be028491e70a30d5e88eba04bc005e641dc23291bae1df8c06f52b42338272029d5e16c3a769a47fb8bb7739f9d9e7661be3209aaae23454fe6075d9a69c202dce61269e267b571a13388a5a31c900feac86c16f458be615e299fbcfdc5c6810686fdfa6ce086cc0cb88b1bc51c7cab56d417418897124f3c949d046f860ae82c71018118f0267382b454fe158040d433ef0fdb760a867a2394b928a6754fef6c0aca93e96fcaea5f88f70f1ca36bca61be2e8ebcef3557d7b2c92493d53dc04effe202ea9c1f6ca97874bd314394ee5fde8ec6d765cfcab93041575bd58257b9d80035cd34113547bc2e3b88f06fba9f13ed74ec9e279478c122a65eab9cecddf0259ca2263bca30a185245e7ff25f3f337c953608a36863f255304ef782ea5a390691e0ce11e469c61cc47e45147f966c8364d103a4b34610b630c1d")
    print("明文：", rData)

