# encoding:utf-8
import json
import os
import shutil
import allure
import pytest
import requests
import pytest_check as check
from ApiTest.AddBug.Zentao_addbug import Zentao
from ApiTest.Comm.Filepath import reportpath
from ApiTest.Comm.Filepath import resultpath
from ApiTest.Comm.Getcasefile import ReadExcel
from ApiTest.Comm.Loginprower import LoginPower
from ApiTest.Comm.Logtype import loggings


casedata = ReadExcel('Data', 'api_test.xlsx', 'Sheet1')
data = casedata.read_data(1, None)
loggings.info('开始执行接口自动化用例')


@pytest.mark.parametrize('datas', data)
@allure.epic('波星通运营管理系统接口测试')
def test_Eeop(datas):
    ss = LoginPower()
    header = ss.loginpower()
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
    case_mmessage = str(json.loads(exceptation)['message'])
    loggings.info('用例编号: ' + case_id + ' 用例标题: ' + case_name)
    loggings.info('请求地址：' + url + ' 请求方式' + method)
    loggings.info('请求参数：' + canshu)
    try:
        req = requests.request(method=method, url=url, headers=header, params=parm)
        check.equal(req.status_code, requests.codes.ok, '发送请求失败,状态码:' + str(req.status_code))

        if req.status_code == 200:
            loggings.info('发送请求成功')
            body = req.json()
            code = body['code']
            message = body['message']
            loggings.info('获取响应code:' + str(code))
            loggings.info('获取响应message:' + message)

            check.equal(str(code), case_code, 'code码不正确' + '响应: ' + str(code) + ', 预期: ' + case_code)
            if str(code) == case_code and message == case_mmessage:
                loggings.info('用例通过')
            else:

                loggings.error('用例不通过')
                loggings.error('捕获响应详情:' + str(body))
                bug = Zentao().addbug('admin', case_name + '接口用例失败', '接口地址:' + url, str(body), exceptation)
                allure.dynamic.description('用例失败，已提交BUG')
                allure.dynamic.issue('bug编号:' + bug[0], 'bug链接:' + bug[1])
        else:
            loggings.error('请求失败')
            loggings.error('失败信息:' + str(req.json()))
            allure.dynamic.description('失败信息:' + str(req.json()))
    except Exception as e:
        loggings.error('捕获异常' + str(e))
        allure.dynamic.description('捕获异常' + str(e))


if __name__ == '__main__':
    reportdir = reportpath()
    resultdir = resultpath()

    pytest.main(["-sv", 'test_boxingtong.py', '--alluredir', resultdir, '--clean-alluredir',
                 '-W', 'ignore:Module already imported:pytest.PytestWarning'])  # 运行指定用例生成测试数据

    shutil.copy('d:/program/ApiTest/Report/environment.properties',
                'd:/program/ApiTest/Report/result/environment.properties')
    os.system('allure generate ' + resultdir + ' -o ' + reportdir + ' --clean')
    loggings.info('用例执行完毕,生成allure测试报告保存至-->>' + reportdir)
