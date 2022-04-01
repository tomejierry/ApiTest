
import time
import jpype

from jpype import *
from ApiTest.Comm.UseJar import JAVA_Public
from ApiTest.Comm.Logtype import loggings

js = JAVA_Public('Data', 'fisher-jmetertoken.jar')
gettoken = js.gettoken()


class LoginPower(object):
    def __init__(self):
        JavaClass_signutil = jpype.JClass('com.birdsh.signtoken.SignUtil')  # 获取JAR包中的CLASS

        self.signutil = JavaClass_signutil()                          # 实例化JAVA方法

        self.map = java.util.HashMap()                                # 实例化JAVA方法

    def loginpower(self):
        t1 = time.time()
        time1 = str(round(t1 * 1000))

        self.map.put('token', gettoken[1])
        self.map.put('timestmap', time1)

        sign = self.signutil.getSign(self.map)                           # 拼接签名
        # loggings.info('获取token：' + gettoken[1])

        header = {'Time-Stamp': time1, 'Sign-Name': str(sign), 'Token': gettoken[1]}

        return header


if __name__ == '__main__':
    power = LoginPower()
    a = power.loginpower()
    print(a)
