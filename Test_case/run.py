
import os
from ApiTest.Comm.Filepath import reportpath
from ApiTest.Comm.Filepath import resultpath
import pytest
from loguru import logger

reportdir = reportpath()
resultdir = resultpath()

logger.info('开始执行接口自动化用例')
if __name__ == '__main__':

    pytest.main(["-s", "-v", './test_boxingtong.py', '--alluredir', resultdir, '--clean-alluredir'])  # 运行指定用例生成测试数据
    # pytest.main(agrs)
    logger.info('用例执行完毕，生成allure测试报告保存至-->>' + reportdir)
    os.system('allure generate ' + resultdir+' -o ' + reportdir + ' --clean')             # 生成ALLURE报告

