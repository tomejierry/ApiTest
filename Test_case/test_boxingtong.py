# encoding:utf-8
import json
import os
import shutil

import allure
import pytest
import requests
from ApiTest.Comm.Filepath import reportpath
from ApiTest.Comm.Filepath import resultpath
from ApiTest.Comm.Getcasefile import ReadExcel
from ApiTest.Comm.Loginprower import LoginPower
from ApiTest.Comm.Logtype import loggings
import pytest_check as check

casedata = ReadExcel('Data', 'api_test.xlsx', 'Sheet1')
data = casedata.read_data(1, None)
loggings.info('开始执行接口自动化用例')


@pytest.mark.parametrize('datas', data)
@allure.epic('波星通运营管理系统')
def test_Eeop(datas):
    allure.dynamic.feature(datas['所属项目'])
    allure.dynamic.story(datas['所属模块'] + '模块')
    allure.dynamic.title('接口: ' + datas['用例编号'] + '-' + datas['用例标题'])

    case_id = datas['用例编号']

    case_name = datas['用例标题']
    url = datas['请求地址']
    method = datas['请求方式']

    dic = datas['请求参数']
    parm = json.loads(dic)
    canshu = str(parm)

    exceptation = datas['期望结果']
    case_code = str(json.loads(exceptation)['code'])

    loggings.info('用例编号: ' + case_id + ' 用例标题: ' + case_name)
    loggings.info('请求地址：' + url + ' 请求方式' + method)
    loggings.info('请求参数：' + canshu)
    ss = LoginPower()
    header = ss.loginpower()

    req = requests.request(method=method, url=url, headers=header, params=parm)

    body = req.json()

    code = body['code']
    message = body['message']

    loggings.info('message:' + message)

    check.equal(str(code), case_code, 'code码不正确' + '响应: ' + str(code) + ', 预期: ' + case_code)


'''  预留安全生产监控平台 
case = casedata.read_data(2, 6)


@pytest.mark.parametrize('cases', case)
@allure.epic('安全生产监控平台')
def test_monitor(cases):
    allure.dynamic.feature(cases['所属项目'])
    allure.dynamic.story(cases['所属模块'] + '模块')
    allure.dynamic.title('接口: ' + cases['用例编号'] + '-' + cases['用例标题'])

    case_id = cases['用例编号']

    case_name = cases['用例标题']
    url = cases['请求地址']
    method = cases['请求方式']

    dic = cases['请求参数']
    parm = json.loads(dic)
    canshu = str(parm)

    exceptation = cases['期望结果']
    case_code = str(json.loads(exceptation)['code'])

    loggings.info('用例编号: ' + case_id + ' 用例标题: ' + case_name)
    loggings.info('请求地址：' + url + ' 请求方式' + method)
    loggings.info('请求参数：' + canshu)
    ss = LoginPower()
    header = ss.loginpower()
    req = requests.request(method=method, url=url, headers=header, params=parm)

    body = req.json()

    code = body['code']
    message = body['message']
    loggings.info('message: ' + message)

    assert case_code == str(code), loggings.error('code码不正确' + '预期: ' + case_code + ', 实际: ' + str(code))  '''

if __name__ == '__main__':
    reportdir = reportpath()
    resultdir = resultpath()

    pytest.main(["-sv", 'test_boxingtong.py', '--alluredir', resultdir, '--clean-alluredir'])  # 运行指定用例生成测试数据

    loggings.info('用例执行完毕,生成allure测试报告保存至-->>' + reportdir)
    shutil.copy('d:/program/ApiTest/Report/environment.properties',
                'D:/program/ApiTest/Report/result/environment.properties')
    os.system('allure generate ' + resultdir + ' -o ' + reportdir + ' --clean')
