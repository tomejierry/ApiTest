# encoding:utf-8

import requests
import allure
import json
import pytest
import os
from ApiTest.Comm.Filepath import reportpath
from ApiTest.Comm.Filepath import resultpath
from ApiTest.Comm.Loginprower import LoginPower
from ApiTest.Comm.Logtype import loggings
from ApiTest.Comm.Getcasefile import ReadExcel
from ApiTest.Comm.UseJar import JAVA_Public
# from ApiTest.Comm.sendemail import sed_mail_more


casedata = ReadExcel('Data', 'api_test.xlsx', 'Sheet1')

case = casedata.read_data(1, 2)


@pytest.mark.parametrize('datas', case)
@allure.epic('这是一个接口测试')
@allure.feature('登录的接口')
def test_loginpower(datas):

    case_id = datas['用例编号']
    case_name = datas['用例标题']
    url = datas['请求地址']
    method = datas['请求方式']

    dic = datas['请求参数']
    parm = json.loads(dic)
    canshu = str(parm)

    yuqi = datas['期望结果']
    case_code = str(json.loads(yuqi)['code'])
    loggings.info('开始执行测试-->>用例编号：' + case_id + ' 用例标题: ' + case_name)
    loggings.info('gettoken：-->>' + url + '请求方式:' + method)
    loggings.info('请求参数' + canshu)

    if case_name == '正确账号密码登陆成功':

        a = LoginPower()

        heard = a.loginpower('http://test1.boxingtong.net:5222/token/loginPower')
        print(heard)
        req = requests.request('GET', 'http://test1.boxingtong.net:5222/token/loginPower', headers=heard)
        body = req.json()
        msg = body['message']
        code = body['code']

        # loggings.info('返回结果：' + str(body))
        loggings.info('message:' + msg)
        assert str(code) == case_code, 'code码不正确：实际结果' + str(code) + ' 预期结果：' + case_code  # 断言code
    else:
        jp = JAVA_Public('Data', 'fisher-jmetertoken.jar')
        header = jp.gettoken()
        request = requests.request(method=method, url=url, headers=header[0], params=parm)
        body = request.json()
        print('返回结果：' + str(body))
        code = body['code']

        loggings.info('message:' + body['message'])
        assert str(code) == case_code, 'code码不正确：实际结果' + str(code) + ' 预期结果：' + case_code  # 断言code


if __name__ == '__main__':
    reportdir = reportpath()
    resultdir = resultpath()
    pytest.main(["-s", "-v", '--alluredir', resultdir, '--clean-alluredir'])              # 运行所有用例生成测试数据

    os.system('allure generate ' + resultdir + ' -o ' + reportdir + ' --clean')    # 生成ALLURE报告
# sed_mail_more('SENDER1', '自动化调试邮件', 1, 2, '测试报告和测试用例', 'Data', 'api_test.xlsx')
