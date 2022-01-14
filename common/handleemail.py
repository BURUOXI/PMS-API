#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time : 2021/12/14 17:43
# @File : handleemail.py
# @Project : PMS-API

import  smtplib
from email.mime.text import MIMEText
from common.handleconf import conf
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart


def send_email(filename,title):


    # 第一步：连接邮箱的smtp服务器，并登录
    smtp = smtplib.SMTP_SSL(host=conf.get("email", "host"), port=conf.getint("email", "port"))
    smtp.login(user=conf.get("email", "user"), password=conf.get("email", "pwd"))

    # 第二步：构建一封邮件
    # 创建一封多组件的邮件
    msg = MIMEMultipart()

    with open(filename, "rb") as f:
        content = f.read()
    # 创建邮件文本内容
    text_msg = MIMEText(content, _subtype="html", _charset="utf8")
    # 添加到多组件的邮件中
    msg.attach(text_msg)
    # 创建邮件的附件
    report_file = MIMEApplication(content)
    report_file.add_header('content-disposition', 'attachment', filename=filename)
    # 将附件添加到多组件的邮件中
    msg.attach(report_file)

    # 主题
    msg["Subject"] = title
    # 发件人
    msg["From"] = conf.get("email", "from_addr")
    # 收件人
    msg["To"] = conf.get("email", "to_addr")

    # 第三步：发送邮箱
    smtp.send_message(msg, from_addr=conf.get("email", "from_addr"), to_addrs=conf.get("email", "to_addr"))