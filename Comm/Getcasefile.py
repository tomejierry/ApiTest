from ApiTest.Comm.Filepath import casepath
from ApiTest.Comm.Logtype import loggings

from openpyxl.styles import PatternFill, colors
import openpyxl
import json
from openpyxl import Workbook


class ReadExcel(object):
    def __init__(self, dirname, filename, sheet_name):
        self.dirname = dirname
        self.filename = casepath(dirname, filename)

        # self.sheet_name = sheet_name
        self.wb = openpyxl.load_workbook(self.filename)  # 获取工作簿对象
        self.sh = self.wb[sheet_name]  # 选择表单

    def read_data(self, start, end):

        """读取数据"""

        datas = list(self.sh.rows)

        # 获取第一行的数据，作为字典的键值
        li1 = []
        for i in datas[0]:
            # print(i.value)
            li1.append(i.value)
        # print(li1)

        # 创建一个空列表，用于存放到用例数据
        cases = []
        # 遍历除第一行之外的数据
        for i in datas[start:end]:  # 切片
            li2 = []

            for c in i:  # 获取该行数据的值
                # values = c.value
                li2.append(c.value)  # 获取每个表格中的数据
            # cases.append(li2)
            # 将该行数据和第一行数据打包，打包转换为字典
            cases.append(dict(zip(li1, li2)))  # 与标题和表格中的数据分装成一个测试用例case,添加到空列表cases中

        return cases

    def write_data(self, real):
        wb2 = openpyxl.Workbook()
        loggings.info('创建一个新的EXCEL')

        sh = wb2[wb2.sheetnames[0]]
        loggings.info('更改默认Sheet名称')
        sh.title = "接口用例"
        wb2.save(casepath(self.dirname, '接口用例测试报告.xlsx'))
        filename = casepath(self.dirname, '接口用例测试报告.xlsx')
        wb2 = openpyxl.load_workbook(filename)
        sheet = wb2['接口用例']  # 获取工作簿对象

        max_row = self.sh.max_row  # 最大行数
        max_column = self.sh.max_column  # 最大列数
        i1 = '%s%d' % (chr(97 + max_column), 1)  # 实际结果行数坐标
        loggings.info('获取测试用例，复写到新的EXCEL')
        for m in range(1, max_row + 1):
            for n in range(97, 97 + max_column):
                n = chr(n)

                i = '%s%d' % (n, m)
                cell1 = self.sh[i].value

                sheet[i].value = cell1  # 赋值到test单元格
        loggings.info('判断表格中实际结果的插入位置列:' + chr(97 + max_column))
        start = 0

        red_fill = PatternFill('solid', fgColor='FF0033')
        green_fill = PatternFill('solid', fgColor='008000')
        yellow_fill = PatternFill('solid', fgColor='FFFF00')
        for number in range(2, max_row + 1):
            for re in real[start]:  # 循环读取实际结果
                i10 = '%s%d' % (chr(97 + max_column), number)

                if re == '失败':  # 根据用例状态改变EXCEL单元格背景颜色
                    sheet[i10].fill = red_fill
                elif re == '通过':
                    sheet[i10].fill = green_fill
                elif re == '异常':
                    sheet[i10].fill = yellow_fill
                else:
                    pass

                sheet[i10].value = re  # 赋值给最后一列

                start += 1
        loggings.info('把执行结果插入到EXCEL中，生成测试结果报告保存在--' + casepath(self.dirname, '接口用例测试报告.xlsx'))
        sheet[i1].value = '实际结果'
        wb2.save(casepath(self.dirname, '接口用例测试报告.xlsx'))  # 保存数据
        wb2.close()


if __name__ == '__main__':
    data = ReadExcel('Data', 'api_test.xlsx', 'Sheet1')
    data.write_data([['失败'], ['异常'], ['通过'], ['失败'], ['失败'], ['通过'], ['结果7'], ['结果8'], ['结果X']])
    #
    # case1 = data.read_data(1, None)
    # print(case1)
