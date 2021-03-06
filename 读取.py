#coding:gbk

import xlrd
from xlrd import xldate_as_tuple
import datetime
'''
xlrd中单元格的数据类型
数字一律按浮点型输出，日期输出成一串小数，布尔型输出0或1，所以我们必须在程序中做判断处理转换
成我们想要的数据类型
0 empty,1 string, 2 number, 3 date, 4 boolean, 5 error
'''

def encryption(num):
    """对数字进行加密解密处理每个数位上的数字变为与7乘积的个位数字，再把每个数位上的数字a变为10-a．"""
    if num==".":
        num=0
    newNum = []

    for i in str(num):
        if(i=="."):
            break
        if int(i):
            newNum.append(str(10 - int(i) * 7 % 10))
        else:
            newNum.append(str(0))

    # print int(''.join(newNum))
    return int(''.join(newNum))



def decryption(num):
    """对数字进行解密处理，把每个数位上的数字乘以7再进行与10求余即可"""
    oldNum = []
    [oldNum.append(str(int(i) * 7 % 10)) for i in str(num)]
    # print int(''.join(oldNum))
    return int(''.join(oldNum))


class ExcelData():
    # 初始化方法
    def __init__(self, data_path, sheetname):
        #定义一个属性接收文件路径
        self.data_path = data_path
        # 定义一个属性接收工作表名称
        self.sheetname = sheetname
        # 使用xlrd模块打开excel表读取数据
        self.data = xlrd.open_workbook(self.data_path)
        # 根据工作表的名称获取工作表中的内容（方式①）
        self.table = self.data.sheet_by_name(self.sheetname)
        # 根据工作表的索引获取工作表的内容（方式②）
        # self.table = self.data.sheet_by_name(0)
        # 获取第一行所有内容,如果括号中1就是第二行，这点跟列表索引类似
        self.keys = self.table.row_values(0)
        # 获取工作表的有效行数
        self.rowNum = self.table.nrows
        # 获取工作表的有效列数
        self.colNum = self.table.ncols

    # 定义一个读取excel表的方法
    def readExcel(self):
        # 定义一个空列表
        datas = []
        for i in range(1, self.rowNum):
            # 定义一个空字典
            sheet_data = {}
            for j in range(self.colNum):
                # print(j)
                # 获取单元格数据类型
                c_type = self.table.cell(i,j).ctype
                # print(c_type)
                # 获取单元格数据
                c_cell = self.table.cell_value(i, j)
                if c_type==1 and j>1 and j!=4:
                    c_cell=float(c_cell)
                    # c_cell=int(c_cell)
                elif c_type == 2 and c_cell % 1 == 0:  # 如果是整形
                    c_cell = int(c_cell)
                elif c_type == 3:
                    date = datetime.datetime(*xldate_as_tuple(c_cell, 0))
                    c_cell = date.strftime('%Y/%m/%d %H:%M:%S')
                elif c_type == 4:
                    c_cell = True if c_cell == 1 else False

                sheet_data[self.keys[j]] = c_cell
                # 循环每一个有效的单元格，将字段与值对应存储到字典中
                # 字典的key就是excel表中每列第一行的字段
                # sheet_data[self.keys[j]] = self.table.row_values(i)[j]
            # 再将字典追加到列表中
            datas.append(sheet_data)
        # 返回从excel中获取到的数据：以列表存字典的形式返回
        return datas
if __name__ == "__main__":
    data_path = "result1.1.xls"
    sheetname = "Sheet1"
    get_data = ExcelData(data_path, sheetname)
    order=get_data.keys
    print(order)
    datas = get_data.readExcel()
    xuehao=input("请输入学号：")
    xuehao=encryption(xuehao)
    flag=0
    for i in range(1,len(datas)):
        if(datas[i]["学号"]==xuehao):
            datas[i]["学号"] = decryption(datas[i]["学号"])
            datas[i]["总分"] = decryption(datas[i]["总分"])
            datas[i]["修正总分"] = decryption(datas[i]["修正总分"])
            datas[i]["编程题总分"] = decryption(datas[i]["编程题总分"])
            datas[i]["程序片段编程题总分"] = decryption(datas[i]["程序片段编程题总分"])
            datas[i]["编程题1"] = decryption(datas[i]["编程题1"])
            datas[i]["编程题2"] = decryption(datas[i]["编程题2"])
            datas[i]["程序片段编程题1"] = decryption(datas[i]["程序片段编程题1"])
            datas[i]["程序片段编程题2"] = decryption(datas[i]["程序片段编程题2"])
            datas[i]["程序片段编程题3"] = decryption(datas[i]["程序片段编程题3"])
            print(datas[i])
            flag=1
    if flag==0:
        print("没有找到学号")



