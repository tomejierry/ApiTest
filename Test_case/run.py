
import os
import shutil
import pytest
import time
from ApiTest.Comm.Filepath import reportpath
from ApiTest.Comm.Filepath import resultpath
from ApiTest.Comm.Logtype import loggings
reportdir = reportpath()
resultdir = resultpath()

if __name__ == '__main__':

    pytest.main(["-s", "-v", './test_boxingtong.py', '--alluredir', resultdir, '--clean-alluredir'])  # 运行指定用例生成测试数据

    loggings.info('用例执行完毕,生成allure测试报告保存至-->>' + reportdir)
    shutil.copy('d:/program/ApiTest/Report/environment.properties',
                'D:/program/ApiTest/Report/result/environment.properties')
    os.system('allure generate ' + resultdir+' -o ' + reportdir + ' --clean')             # 生成ALLURE报告

