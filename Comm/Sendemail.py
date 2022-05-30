import smtplib
import os
from ApiTest.Comm.ReadConfig import ReadConfig

from ApiTest.Comm.Filepath import *
from ApiTest.Comm.Logtype import loggings
from email.mime.text import MIMEText  # 发送字符串引入
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart  # 处理多种形态的邮件主体需要 MIMEMultipart 类
from email.mime.image import MIMEImage  # 处理图片需要 MIMEImage 类


def sed_mail_more(pamr):
    msg = MIMEMultipart()
    se = ReadConfig().read_config('ADDRESSEE')
    adds = list(dict(se).values())[pamr['star']:pamr['end']]  # 取出配置文件中需要的收件人信息并装载到列表，切片读取
    sends = dict(ReadConfig().read_config(pamr['SENDER']))  # 发件人信息转换成字典

    sender = sends['sender']
    pwd = sends['code']
    smtp = sends['smtp']
    msg.attach(MIMEText(pamr['body_s']))  # 加载正文

    zip1 = pamr['allurepath']
    if len(zip1) > 0:
        loggings.info('本次发送allure程序包，用时时间稍长')
        allurezip = MIMEApplication(open(zip1, 'rb').read())  # allure程序zip包
        allurezip.add_header('Content-Disposition', 'attachment', filename='allure.zip')
        msg.attach(allurezip)  # 加载allure程序附件
    else:
        loggings.info('本次不发送allure程序包')

    zip2 = os.path.join(reportpath() + '.zip')  # allure报告路径
    htmlzip = MIMEApplication(open(zip2, 'rb').read())  # 报告附件zip包
    htmlzip.add_header('Content-Disposition', 'attachment', filename='html.zip')
    msg.attach(htmlzip)  # 加载allure报告附件

    annex = casepath(pamr['dirname'], pamr['filename'])  # 用例路径报告
    att = MIMEApplication(open(annex, 'rb').read())  # 用例报告附件
    att.add_header('Content-Disposition', 'attachment', filename='api_test.xlsx')
    msg.attach(att)  # 加载用例报告附件

    readme = casepath(pamr['dirname'], pamr['readme'])
    readme_allure = MIMEApplication(open(readme, 'rb').read())  # ALLURE报告使用说明
    readme_allure.add_header('Content-Disposition', 'attachment', filename='readme_allure.doc')
    msg.attach(readme_allure)

    msg['Subject'] = pamr['subjects']  # 邮件主题
    msg['From'] = sender  # 发送方信息
    loggings.info('登录邮箱---->' + '邮箱服务器:' + smtp + ',' + '账号:' + sender)
    try:
        server = smtplib.SMTP(smtp)  # 邮箱服务器地址
        server.login(sender, pwd)
        loggings.info('发送邮件---->' + '收件人:' + str(adds) + ',' + '邮件主题:' + pamr['subjects'] + ',' + '正文内容:' + pamr['body_s'])
        server.sendmail(sender, adds, msg.as_string())
        print('success')
        server.quit()
        loggings.info('关闭邮箱')

    except smtplib.SMTPException as e:
        loggings.error(str(e))
        print('error', e)


# if __name__ == "__main__":
    # sed_mail_more({
    #     "SENDER": "SENDER1",
    #     "subjects": "接口自动化测试报告",
    #     "star": 1,
    #     "end": 2,
    #     "body_s": "测试完成",
    #     "dirname": "Data",
    #     "filename": "接口用例测试报告.xlsx",
    #     "readme": "readme_allure.doc",
    #     "allurepath": ""    # 此处传入allure程序zip包路径则发送，空字符串""不发送zip包
    # })
