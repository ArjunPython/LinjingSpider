# -*- coding: utf-8 -*-
# author: Arjun
# @Time: 18-9-17 上午9:26

import smtplib
import datetime
from email.mime.text import MIMEText


class EmailSender(object):

    def __init__(self):
        self.smtp_host = "smtp.163.com"      # 发送邮件的smtp服务器（从QQ邮箱中取得）
        self.smtp_user = "xxxxxx" # 用于登录smtp服务器的用户名，也就是发送者的邮箱
        self.smtp_pwd = "xxxxxx"  # 授权码，和用户名user一起，用于登录smtp， 非邮箱密码
        self.smtp_port = 465            # smtp服务器SSL端口号，默认是465
        self.sender = "xxxxxx"    # 发送方的邮箱

    def sendEmail(self, toList, subject, body):
        '''
        发送邮件
        :param toLst: 收件人的邮箱列表[]
        :param subject: 邮件标题
        :param body: 邮件内容
        :return:
        '''
        message = MIMEText(body, 'plain', 'utf-8')  # 邮件内容，格式，编码
        message['From'] = self.sender               # 发件人
        message['To'] = ",".join(toList)             # 收件人列表
        message['Subject'] = subject                # 邮件标题
        try:
            smtpSSLClient = smtplib.SMTP_SSL(self.smtp_host, self.smtp_port)   # 实例化一个SMTP_SSL对象
            loginRes = smtpSSLClient.login(self.smtp_user, self.smtp_pwd)      # 登录smtp服务器
            if loginRes and loginRes[0] == 235:
                print("登录成功")
                smtpSSLClient.sendmail(self.sender, toList, message.as_string())
                print("mail has been send successfully")
            else:
                print("登陆失败")
        except Exception as e:
            print("发送失败，Exception: e=%s" % e)