
from ApiTest.Comm.Filepath import casepath
from ApiTest.Comm.Logtype import loggings
import openpyxl


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

    # copy_excel('D:\\workingpaper\\test.xlsx')
    print(case1)
