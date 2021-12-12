# encoding:utf-8
import jpype
import time

import requests
from jpype import *
from ApiTest.Comm.Howrequest import call
from ApiTest.Comm.Filepath import casepath


class JAVA_Public(object):

    def __init__(self, filename, dirname):
        self.jar_path = casepath(filename, dirname)

        self.jvm_Path = 'D:/program/JAVA/bin/server/jvm.dll'
        try:

            jpype.startJVM(self.jvm_Path, '-Djava.class.path=%s' % self.jar_path)  # 启动JAVA环境
        except:
            pass

        self.JavaClass_signutil = jpype.JClass('com.birdsh.signtoken.SignUtil')  # 获取JAR包中的CLASS
        self.JavaClass_newmd5encrypt = jpype.JClass('com.birdsh.signtoken.NewMD5Encrypt')

        self.map = java.util.HashMap()

        self.newmd5 = self.JavaClass_newmd5encrypt()
        self.signutil = self.JavaClass_signutil()

    def gettoken(self):
        t = time.time()
        pctime = str(round(t * 1000))  # 13位时间戳

        pctoken = self.newmd5.MD5Encode(pctime)  # 加密时间戳生成token

        self.map.put('timestamp', pctime)

        self.map.put('token', pctoken)
        pcsign = self.signutil.getSign(self.map)

        header = {'Time-Stamp': pctime, 'Sign-Name': str(pcsign), 'Token': str(pctoken)}
        parm = {'username': 'tao.yue', 'password': '8b7fb7faba5d48ce352be71e798336', 'type': 0,
                'sign': 'e37c848e62e3d7157741546d2fff85b2'}

        request = requests.request(method='post', url='http://test1.boxingtong.net:5222/token/getToken',
                                   headers=header, params=parm)
        body = request.json()
        # print(body)

        token = body['data']['tocken']
        # print(token)

        return header, token

#
# if __name__ == "__main__":
#     java = JAVA_Public('Data', 'fisher-jmetertoken.jar')
#
#     a = java.gettoken()
#     jpype.shutdownJVM()  # 关闭JAVA环境

