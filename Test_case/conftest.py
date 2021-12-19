# conftest.py
from _pytest.config import hookimpl
# import re
# import pytest
# import allure
# from ApiTest.Comm.Logtype import loggings
# from ApiTest.AddBug.Zentao_addbug import Zentao
# from ApiTest.Comm.Getcasefile import ReadExcel
#
#
# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# def pytest_runtest_makereport(item, call):
#     # 获取钩子方法的调用结果
#     out = yield
#     # print('用例执行结果', out)
#
#     # 3. 从钩子方法的调用结果中获取测试报告
#     report = out.get_result()
#
#     if report.when == "call" and report.outcome == 'failed':
#         casedata = ReadExcel('Data', 'api_test.xlsx', 'Sheet1')
#         data = casedata.read_data(0, None)
#         ex = '{}'.format(call.excinfo) + 'yc'
#         ex1 = ex
#         # exo = re.findall(r'异常(.+?)>yc', ex)
#         loggings.error('捕获异常' + ex)
#         case = '{}'.format(item)
#         case_num = re.findall(r'datas(.+?)]', case)
#         case_name = data[int(case_num[0])]['用例标题']
#         url = data[int(case_num[0])]['请求地址']
#         ext = data[int(case_num[0])]['期望结果']
#         loggings.error('用例不通过')
#         bug = Zentao().addbug('admin', case_name + '接口用例失败', '接口地址:' + url, ex1, ext)
#         allure.dynamic.description('用例失败，已提交BUG')
#         allure.dynamic.issue('bug编号:' + bug[0], 'bug链接:' + bug[1])
#         pass


