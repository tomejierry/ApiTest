# encoding:utf-8

import json
import allure
import pytest
import requests
from ApiTest.Comm.Logtype import loggings
from ApiTest.Comm.Getcasefile import ReadExcel
from ApiTest.Comm.Loginprower import LoginPower


casedata = ReadExcel('Data', 'api_test.xlsx', 'Sheet1')
case = casedata.read_data(1, None)


@pytest.mark.parametrize('datas', case)
@allure.epic('接口自动化测试')
def test_boxingtong(datas):
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
    loggings.info('message: ' + message)

    assert case_code == str(code), loggings.error('code码不正确' + '预期: ' + case_code + ', 实际: ' + str(code))


if __name__ == '__main__':
    pytest.main(['-s', '-v'])
