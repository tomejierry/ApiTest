# conftest.py
import operator

from _pytest.config import hookimpl
import time
from _pytest import terminal
import re
from ApiTest.Config.case_cfg import *
from ApiTest.Comm.Logtype import loggings
from ApiTest.Comm.Getcasefile import ReadExcel


# @pytest.hookimpl(hookwrapper=True, tryfirst=True)
# def pytest_runtest_makereport(item, call):
#     # 获取钩子方法的调用结果
#     out = yield
#     # print('用例执行结果', out)
#     #
#     #     # 3. 从钩子方法的调用结果中获取测试报告
#     report = out.get_result()
#     # print(report)
#     #


def pytest_terminal_summary(terminalreporter, exitstatus, config):
    """ 收集测试结果的钩子函数，用做后续结果统计处理 """

    # report = terminalreporter.stats['']

    loggings.info('获取所有测试用例执行结果')
    #
    passed = terminalreporter.stats.get('passed', [])
    failed = terminalreporter.stats.get('failed', [])
    error = terminalreporter.stats.get('error', [])
    # print(f'pass--{passed}')
    # print(f'fail--{failed}')
    # print(f'error--{error}')
    report_list = []  # 封装不同状态的测试结果到列表
    if len(passed) > 0:

        for p in passed:
            p1 = [p]
            report_list.append(p1)
    if len(failed) > 0:
        for f in failed:
            f1 = [f]
            report_list.append(f1)

    if len(error) > 0:
        for e in error:
            e1 = [e]

            report_list.append(e1)

    # print(report_list)
    list_all = []
    project_list = []
    for r1 in report_list[0:]:
        projects = re.findall(r'::test_(.*?)\[data', str(r1))  # 正则提取测试函数名称
        ret = re.findall(r"outcome='(.+?)'>", str(r1))  # 正常提取测试结果
        n = re.findall(r'\d+', str(r1))  # 正则提取用例编号初始编号为0
        project_list.append(projects[0])  # 装载测试函数名称到列表
        d = [int(n[0]) + 1, projects[0], ret[0]]
        list_all.append(d)  # 装载用例编号，函数名称，测试结果到总列表

    list_1 = sorted(set(project_list), key=project_list.index)
    ll = []
    for i in range(0, len(list_1)):
        for ii in list_all:
            if list_1[i] == ii[1]:
                ll.append(ii)  # 把相同的测试函数单独装载的列表中

    count_list = []
    for c in list_1:
        count_list.append(project_list.count(c))  # 统计每个测试函数的数量，装载到列表
    start = 0
    real1 = []
    for nb1 in count_list:
        real = ll[start:start + nb1]
        real1.append(real)  # 根据函数的执行数量进行切片分割，得到每个函数的所有结果
        start += nb1

    for iii in range(0, len(list_1)):
        # print(real1[ii])
        lll = real1[iii]
        lll.sort(key=lambda x: x[0])  # 根据用例编号排序

        loggings.info('把测试结果处理完成后，封装成列表嵌套列表格式:[[],[],...]')
        loggings.info(f'第{iii + 1}个测试函数test_{list_1[iii]}的所有结果--->{real1[iii]}')
        loggings.info('调用接口，把执行结果反写到测试用例中:write_data')
        print(f'-----------------------{globals()[list_1[iii] + "_casecfg"]()}')
        data = ReadExcel(globals()[list_1[iii] + '_casecfg']())
        report_name = list_1[iii] + '接口用例测试报告.xlsx'
        data.write_data(lll, report_name)

    # print('failed:', len(terminalreporter.stats.get('failed', [])))
    # print('error:', len(terminalreporter.stats.get('error', [])))
    # print('skipped:', len(terminalreporter.stats.get('skipped', [])))
    # terminalreporter._sessionstarttime 会话开始时间
    # duration = time.time() - terminalreporter._sessionstarttime
    # print('total times:', duration, 'seconds')
