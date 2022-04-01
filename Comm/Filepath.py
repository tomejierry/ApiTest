import os
import time

time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))   # 把当前时间转换时间格式

'''
把文件路径进行封装， 调用方法获取用例，保存日志、报告等。
'''


def casepath(dirname, filename):
    """

    :param dirname:
    :param filename:
    :return:
    """
    a = os.path.dirname(__file__)
    b = os.path.dirname(a)
    c = os.path.join(b, dirname, filename)
    return c


def screen():
    """

    :return:
    """
    a = os.path.dirname(__file__)
    b = os.path.dirname(a)
    s = os.path.dirname(b)
    c = os.path.join(s, 'UITEST', 'Report', 'screenshot\\testUI_')
    screen_save_path = c + time     # 用时间格式进行命名文件

    return screen_save_path
#
# a = screen()
# print(a)



# def logpath():
#     a = os.path.dirname(__file__)
#     b = os.path.dirname(a)
#     c = os.path.join(b, 'LOG', '.log')
#     return c


def reportpath():
    """

    :return:
    """
    a = os.path.dirname(__file__)
    b = os.path.dirname(a)
    c = os.path.join(b, 'Report', 'html')
    return c



def resultpath():
    """

    :return:
    """
    a = os.path.dirname(__file__)
    b = os.path.dirname(a)
    c = 'D:/program/tomcat9/webapps/Jenkins/.jenkins/workspace/API_test/allure-results'
    return c


def Configlpath():
    """

    :return:
    """
    a = os.path.dirname(__file__)
    b = os.path.dirname(a)
    c = os.path.join(b, 'Config', 'config.ini')
    return c

# ss = resultpath ()
# print(ss)
