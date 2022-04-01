
import os
import shutil
import pytest
import time
from ApiTest.Comm.Filepath import reportpath
from ApiTest.Comm.Filepath import resultpath
from ApiTest.Comm.Logtype import loggings

# reportdir = reportpath()
# resultdir = resultpath()

if __name__ == '__main__':
    reportdir = reportpath()
    resultdir = resultpath()
    pytest.main(["-sv", 'test_EEOP.py', '--alluredir', resultdir, '--clean-alluredir',
                 '-W', 'ignore:Module already imported:pytest.PytestWarning'])  # 运行指定用例生成测试数据

    shutil.copy('d:/program/ApiTest/Report/environment.properties',
                'd:/program/ApiTest/Report/result/environment.properties')
    os.system('allure generate ' + resultdir + ' -o ' + reportdir + ' --clean')
    loggings.info('用例执行完毕,生成allure测试报告保存至-->>' + reportdir)
    # from ApiTest.Comm.Zip import zipDir
    # zipDir(reportpath(), reportpath()+'.zip')   # 将报告打包成zip
    # from ApiTest.Comm.Sendemail import sed_mail_more
    # sed_mail_more({
    #     "SENDER": "SENDER1",
    #     "subjects": "接口自动化测试报告",
    #     "star": 1,
    #     "end": 2,
    #     "body_s": "测试完成",
    #     "dirname": "Data",
    #     "filename": "接口用例测试报告.xlsx",
    #     "readme": "readme_allure.doc",
    #     "allurepath": ""  # 此处传入allure程序zip包路径则发送，空字符串""不发送zip包
    # })
    # os.system('allure open -h 127.0.0.1 -p 8282 ' + reportpath())


