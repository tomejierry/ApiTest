
import os
# import subprocess
from ApiTest.Comm.Filepath import reportpath
from ApiTest.Comm.Filepath import resultpath
import pytest
# from loguru import logger

reportdir = reportpath()
resultdir = resultpath()

# logger.info('开始执行接口自动化用例')
if __name__ == '__main__':

    pytest.main(["-s", "-v", './test_login.py', '--alluredir', resultdir, '--clean-alluredir'])  # 运行指定用例生成测试数据
    # pytest.main(agrs)
    os.system('allure generate ' + resultdir+' -o ' + reportdir + ' --clean')             # 生成ALLURE报告


# os.system('allure open -h 127.0.0.1 -p 63342'+reportdir+'')                    # 打开报告==不知道为什么打不开指定的报告
# subprocess.call('allure open -h 127.0.0.1 -p 63342'+reportdir+'',shell=True)   #   这个方法也不行
