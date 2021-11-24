
from ApiTest.Comm.Filepath import casepath

import openpyxl
from ApiTest.Comm.Logtype import loggings


def copy_excel(newfile_path):

    """ 复制一个表格的数据，写入到另一个新表中 """

    # 新建excel
    wb2 = openpyxl.Workbook()
    wb2.save(newfile_path)
    print('新建成功')

    # 读取数据

    case = casepath('Data', 'case.xlsx')
    wb1 = openpyxl.load_workbook(case)

    wb2 = openpyxl.load_workbook(newfile_path)

    sheet1 = wb1['Sheet1']
    sheet2 = wb2['Sheet1']

    max_row = sheet1.max_row  # 最大行数
    max_column = sheet1.max_column  # 最大列数

    for m in range(1, max_row + 1):
        for n in range(97, 97 + max_column):  # chr(97)='a'
            n = chr(n)  # ASCII字符
            i = '%s%d' % (n, m)  # 单元格编号
            cell1 = sheet1[i].value  # 获取data单元格数据
            sheet2[i].value = cell1  # 赋值到test单元格

    wb2.save(newfile_path)  # 保存数据
    wb1.close()  # 关闭excel
    wb2.close()


class ReadExcel(object):
    def __init__(self, dirname, filename, sheet_name):

        self.filename = casepath(dirname, filename)
        loggings.info('用例From:' + self.filename)
        self.sheet_name = sheet_name
        self.wb = openpyxl.load_workbook(self.filename)  # 获取工作簿对象
        self.sh = self.wb[self.sheet_name]  # 选择表单

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


if __name__ == '__main__':
    data = ReadExcel('Data', 'api_test.xlsx', 'Sheet1')

    case1 = data.read_data(1, None)

    copy_excel('D:\\workingpaper\\test.xlsx')
    print(case1)
