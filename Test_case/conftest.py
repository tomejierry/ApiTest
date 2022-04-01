# conftest.py

from Comm.Filepath import casepath
from _pytest.config import hookimpl
import time
from _pytest import terminal
import re

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
    # print(f"全部报告：{report}")
    # ss = str(report)
    # print(type(ss))
    loggings.info('获取所有测试用例执行结果')
    passed = terminalreporter.stats.get('passed', [])
    failed = terminalreporter.stats.get('failed', [])
    error = terminalreporter.stats.get('error', [])
    loggings.info('创建一个空列表，收集中测试用例编号，结果类型')
    ls = []

    if len(passed) > 0:   # 判断结果类型是否存在，存在读取结果和用例编号，不存在跳过

        for i in passed:
            p = str(i)
            n = re.findall(r'\d+', p)
            m = int(n[0]) + 1     # 处理用例编号
            # r = re.findall(r"outcome='(.*?)'", p)
            r = '通过'            # 自定义passed状态的输出文案
            list1 = [m, r]
            ls.append(list1)
    else:
        pass
    if len(failed) > 0:  # 判断结果类型是否存在，存在读取结果和用例编号，不存在跳过
        for ii in failed:
            f = str(ii)
            nn = re.findall(r'\d+', f)
            mm = int(nn[0]) + 1            # 处理用例编号
            # rr = re.findall(r"outcome='(.*?)'", f)
            rr = '失败'     # 自定义failed状态的输出文案
            list2 = [mm, rr]
            ls.append(list2)
    else:
        pass
    if len(error) > 0:  # 判断结果类型是否存在，存在读取结果和用例编号，不存在跳过
        for iii in error:
            er = str(iii)
            nnn = re.findall(r'\d+', er)
            mmm = int(nnn[0] + 1)         # 处理用例编号
            rrr = '异常'            # 自定义error状态的输出文案
            list3 = [mmm, rrr]
            ls.append(list3)
    else:
        pass

    ls.sort(key=(lambda x: x[0]))   # 根据测试用例编号重新排序
    real = []
    for iiii in ls:
        real.append([iiii[1]])
    loggings.info('把测试结果处理完成后，封装成列表嵌套列表格式:[[],[],...]')
    loggings.info('调用接口，把执行结果反写到测试用例中:weite_data')
    data = ReadExcel('Data', 'api_test.xlsx', 'Sheet1')
    data.write_data(real)

    # print('failed:', len(terminalreporter.stats.get('failed', [])))
    # print('error:', len(terminalreporter.stats.get('error', [])))
    # print('skipped:', len(terminalreporter.stats.get('skipped', [])))
    # terminalreporter._sessionstarttime 会话开始时间
    # duration = time.time() - terminalreporter._sessionstarttime
    # print('total times:', duration, 'seconds')
