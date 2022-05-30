# encoding:utf-8
import json
import shutil
import allure
import pytest
import requests
import pytest_check as check
from ApiTest.AddBug.Zentao_addbug import Zentao
from ApiTest.Comm.Filepath import *

from ApiTest.Comm.Getcasefile import ReadExcel
from ApiTest.Comm.Loginprower import LoginPower
from ApiTest.Comm.Logtype import loggings
from ApiTest.Config.case_cfg import *

casedata = ReadExcel(EEOP_casecfg())
data = casedata.read_data()
loggings.info('开始执行接口自动化用例')


class Test_Apicase:

    @pytest.mark.parametrize("datas", data)
    @allure.epic('波星通运营管理系统接口测试')
    def test_EEOP(self, datas):
        header = LoginPower().loginpower()
        allure.dynamic.feature(datas['所属项目'])
        allure.dynamic.story(datas['所属模块'] + '模块')
        allure.dynamic.title(f'接口: {datas["用例编号"]}-{datas["用例标题"]}')

        case_id = datas['用例编号']
        case_name = datas['用例标题']
        url = datas['请求地址']
        method = datas['请求方式']

        dic = datas['请求参数']
        parm = json.loads(dic)

        exceptation = datas['期望结果']

        case_code = str(json.loads(exceptation)['code'])
        case_mmessage = str(json.loads(exceptation)['message'])
        loggings.info('用例编号: %r,用例标题: %r,请求地址: %r,请求方式: %r,请求参数: %r' % (case_id, case_name, url, method, dic))

        try:

            req = requests.request(method=method, headers=header, url=url, params=parm)

            check.equal(req.status_code, requests.codes.ok, f'发送请求失败,状态码:{req.status_code}')

            if req.status_code == 200:
                loggings.info('发送请求成功')
                body = req.json()

                code = body['code']
                message = body['message']
                loggings.info(f'获取响应code:{code}')
                loggings.info(f'获取响应message:{message}')

                check.equal(str(code), case_code, f'code码不正确,响应{code},预期{case_code}')
                if str(code) == case_code and message == case_mmessage:
                    loggings.info('用例通过')

                else:

                    loggings.error('用例不通过')
                    loggings.error(f'捕获响应详情:{body}')
                    # bug = Zentao().addbug('admin', case_name + '接口用例失败', '接口地址:' + url, str(body), exceptation)
                    # allure.dynamic.description('用例失败，已提交BUG')
                    # allure.dynamic.issue('bug编号:' + bug[0], 'bug链接:' + bug[1])

            else:
                loggings.error('请求失败')
                loggings.error(f'失败信息:{req.json()}')
                allure.dynamic.description('失败信息:' + str(req.json()))

        except Exception as e:
            loggings.error(f'捕获异常:{e}')
            allure.dynamic.description('捕获异常' + str(e))


if __name__ == "__main":
    reportdir = reportpath()
    resultdir = resultpath()

    pytest.main(["-sv", 'test_EEOP.py', '--alluredir', resultdir, '--clean-alluredir',
                 '-W', 'ignore:Module already imported:pytest.PytestWarning'])  # 运行指定用例生成测试数据

    shutil.copy('d:/program/ApiTest/Report/environment.properties',
                'd:/program/ApiTest/Report/result/environment.properties')
    os.system('allure generate ' + resultdir + ' -o ' + reportdir + ' --clean')
    loggings.info('用例执行完毕,生成allure测试报告保存至-->>' + reportdir)
