import time
import requests
from lxml import etree
from ApiTest.Comm.Logtype import loggings


host = "http://127.0.0.1"


class Zentao:
    def __init__(self):
        self.s = requests.session()
        self.head = {"Content-Type": "application/x-www-form-urlencoded"
                     }

    def login(self, user="admin", password="yuetao521"):
        '''
        禅道登录
        :param user:        登录用户
        :param password:    登录密码
        :return:            返回数据 - 服务端
        '''

        url = host + "/zentao/user-login.html"

        body = {"account": user,
                "password": password,
                "referer": host + "/zentao/my/",
                "keepLogin": 1
                }
        get_sid = requests.get(url)
        SID = get_sid.cookies["zentaosid"]
        loginCookies = dict(zentaosid=SID, lang='zh-cn', keepLogin='on')
        loggings.info('登录禅道-->账号:' + user)
        r = self.s.post(url, headers=self.head, data=body, cookies=loginCookies)
        if "self.location=" in r.content.decode():
            token = r.cookies['zp']
            loggings.info(str(r.status_code) + "-->登录成功!")
            return token, r.cookies
        elif "登录失败，请检查您的用户名或密码是否填写正确" in r.content.decode:
            loggings.error("登录失败，用户名或密码不对")

        else:
            loggings.error("登录失败，其它问题：%s" % r.content.decode)

    def addbug(self, touser, title, step, result, expect):

        urls = host + "/zentao/bug-create-2-0-moduleID=0.html"
        cookie = Zentao().login()[1]
        # text_1 = requests.get(urls, cookies=cookie).text
        # uid = re.findall("var kuid = '(.*?)';", text_1)[0]  # 获取UID
        # loggings.info('获取uid:' + uid)
        data = {
            "product": "2",               # int 所属产品  * 必填
            "module": "1",                # int 所属模块
            "project": "1",               # int 所属项目
            "openedBuild[]": "trunk",     # int | trunk 影响版本 * 必填
            "assignedTo": touser,         # string 指派给
            "type": "codeerror",          # bug类型
            "os": "",                     # 操作系统
            "browser": "",                # 浏览器
            "color": "",
            "title": title,
            "severity": "3",              # int 严重程度 取值范围：1 | 2 | 3 | 4
            "pri": "3",                   # int 优先级 取值范围：0 | 1 | 2 | 3 | 4
            "steps":
                '<p>[步骤]</p>' + step +
                '<p>[结果]</p>' + result +
                '<p>[期望]</p>' + expect,   # string 重现步骤
            "story": "0",                  # 相关需求
            "task": "0",                   # 相关任务
            # "mailto[]": "",
            # "keywords": "",              # string 关键词
            # "files[]": "",               # 上传文件
            # "labels[]": "",
            # "uid": uid,
            "case": "0",
            "caseVersion": "0",
            "result": "0",
            "testtask": "0"
        }
        file = {
            "files[]": ("1628129567.png",
                        open("C:/Users/tomejierry/Pictures/Saved Pictures/1628129567.png", "rb"), "image/png")

        }
        loggings.info('提交BUG--> 标题:' + title)
        loggings.info('指派-->' + touser)
        result = requests.post(urls, data=data, headers=self.head, cookies=cookie)

        if '保存成功' in result.text:
            loggings.info('提交BUG成功')
            time.sleep(3)
            url = host + "/zentao/bug-browse-2-0-unclosed.html"

            r = requests.get(url, headers=self.head, cookies=cookie)
            er = etree.HTML(r.text)

            bugid = er.xpath('/html/body/main/div/div[3]/div[2]/form/div[2]/table/tbody/tr[1]/td[1]/a')[0].text
            href = er.xpath("/html/body/main/div/div[3]/div[2]/form/div[2]/table/tbody/tr[1]/td[1]/a/@href")
            buglink = host + href[0]

            loggings.info('bugID:' + bugid)
            loggings.info('bug链接:' + buglink)
            return bugid, buglink
        else:
            loggings.error('提交BUG失败' + result.text)


# if __name__ == '__main__':
#     Zentao().addbug('admin', 'testbug074', '步骤1', '结果1', '期望1')


