import smtplib
import os
from ApiTest.Comm.ReadConfig import ReadConfig
from ApiTest.Comm.Filepath import reportpath
from ApiTest.Comm.Filepath import casepath
from ApiTest.Comm.Logtype import loggings
from email.mime.text import MIMEText  # 发送字符串引入
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart  # 处理多种形态的邮件主体我们需要 MIMEMultipart 类
from email.mime.image import MIMEImage  # 处理图片需要 MIMEImage 类


def sed_mail_more(SENDER, subjects, star, end, body_s, dirname, filename):
    msg = MIMEMultipart()
    se = ReadConfig().read_config('ADDRESSEE')
    adds = list(dict(se).values())  # 取出配置文件中所有的收件人信息并装载到列表

    add = adds[star:end]  # 配置收件人从第几位到第几位

    sends = ReadConfig().read_config(SENDER)

    send = dict(sends)

    sender = send['sender']
    pwd = send['code']
    smtp = send['smtp']
    msg.attach(MIMEText(body_s))

    ss = os.path.join(reportpath(), 'index.html')

    body = MIMEApplication(open(ss, 'rb').read())  # 邮件内容设置正文到容器
    body.add_header('Content-Disposition', 'attachment', filename='allure.html')
    msg.attach(body)

    annex = casepath(dirname, filename)  # 附件内容的路径
    att = MIMEApplication(open(annex, 'rb').read())  # 邮件附件

    att.add_header('Content-Disposition', 'attachment', filename='case.xlsx')

    msg.attach(att)

    msg['Subject'] = subjects  # 邮件主题

    msg['From'] = sender  # 发送方信息
    loggings.info('登录邮箱---->' + '邮箱服务器:' + smtp + ',' + '账号:' + sender + ',' + '授权码:' + pwd)
    try:
        server = smtplib.SMTP(smtp)  # 邮箱服务器地址
        server.login(sender, pwd)
        loggings.info('发送邮件---->' + '收件人:' + str(add) + ',' + '邮件主题:' + subjects + ',' + '正文内容:' + body_s)
        server.sendmail(sender, add, msg.as_string())
        print('success')
        server.quit()
        loggings.info('关闭邮箱')

    except smtplib.SMTPException as e:
        loggings.error(str(e))
        print('error', e)


# sed_mail_more('SENDER1', '自动化调试邮件', 1, 2, '测试报告和测试用例', 'Data', 'case.xlsx')
