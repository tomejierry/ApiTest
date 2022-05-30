
import time
import jpype
import requests
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

        header = {"Time-Stamp": time1, "Sign-Name": str(sign), "Token": gettoken[1]}

        return header


def APP_gettoken():
    url = 'http://test1.boxingtong.net:8001/user/login'
    method = 'POST'
    parm = {
        "userName": "15921104378",
        "force": "0",
        "password": "e9adc3141ba51abbe56ea57f2f883e",
        "passwordHst": "e10adc3949ba59abbe56e057f20f883e",
        "model": "TEL-AN10",
        "isBird": "false"
    }
    try:
        loggings.info('登陆波星通，获取token')
        req = requests.request(method=method, url=url, params=parm)
        body = req.json()
        code = body['code']
        if code == 1:
            token = body['data']['token']
            cid = body['data']['cid']
            mac = body['data']['macAddr']
            header = {'token': token, 'cid': cid, 'BIRD-MAC-ADDRESS': mac}
            return header
        else:
            return '登陆失败，无法获取token'
    except Exception as e:
        loggings.error(f'请求失败{e}')

if __name__ == '__main__':
    # power = LoginPower()
    # a = power.loginpower()
    # print(a)
    print(APP_gettoken())