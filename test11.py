# -*- coding: utf-8 -*-            
# @Time : 2022/6/2 16:24
# @Author:mr.Zhang
# @FileName: test11.py
# @Software: PyCharm
def test():
    a = ["鲁AU2689", "鲁AH7K70", "鲁AX1102", "鲁AX3375", "鲁AM8612", "鲁AU8238", "鲁AX3580", "鲁AW7830", "鲁AX6225", "鲁AD5848",
         "鲁AX0096", "鲁AM8878",
         "鲁AA2388", "鲁AU2598", "鲁AU7588", "鲁AA2097", "鲁AU0667", "鲁AU2689", "鲁AX3809", "鲁AR2773", "鲁AX3580", "鲁AU6529",
         "鲁A1J08L", "鲁AR2773",
         "鲁H63X01", "鲁AX0096", "鲁AW7830", "鲁AU6529", "鲁AX1067", "鲁AM9759", "鲁AX1211", "鲁AL7573", "鲁AU4398", "鲁AX6225",
         "鲁AD5848", "鲁AW9032",
         "鲁AU0961", "鲁AX1211", "鲁AX1067", "鲁AE2119", "鲁AX9720", "鲁AA2097", "鲁AU9293", "鲁AD9408", "鲁AM8878", "鲁AW9032",
         "鲁AD8077", "鲁AU6703",
         "鲁AX1211", "鲁AX9720", "鲁AW9032", "鲁AX5368", "鲁AU8238", "鲁AV6148", "鲁AX6225", "鲁AF9790", "鲁AD5848", "鲁AX0096",
         "鲁AX6225", "鲁AW9723",
         "鲁AX0060", "鲁AU2598", "鲁AU7588", "鲁AX9720", "鲁AV2997", "鲁AM8878", "鲁AV3760"]
    b = list(set(a))
    print(len(b))
    # ['鲁AX3809', '鲁AV3760', '鲁AX1211', '鲁AA2097', '鲁AX9720', '鲁AE2119', '鲁H63X01', '鲁AU8238', '鲁AU2689', '鲁AM8878',
    #  '鲁AX3375', '鲁AM9759', '鲁AX0096', '鲁A1J08L', '鲁AU6529', '鲁AU2598', '鲁AF9790', '鲁AX3580', '鲁AV2997', '鲁AU0667',
    #  '鲁AM8612', '鲁AD9408', '鲁AX0060', '鲁AL7573', '鲁AW9723', '鲁AW9032', '鲁AH7K70', '鲁AU7588', '鲁AX1102', '鲁AX5368',
    #  '鲁AU0961', '鲁AD8077', '鲁AW7830', '鲁AA2388', '鲁AR2773', '鲁AD5848', '鲁AU4398', '鲁AX6225', '鲁AU9293', '鲁AV6148',
    #  '鲁AU6703', '鲁AX1067']


if __name__ == '__main__':
    test()