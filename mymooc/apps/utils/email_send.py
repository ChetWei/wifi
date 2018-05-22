# -*- coding: utf-8 -*-
# @Time    : 2018/4/17 12:42
# @Author  : Wei
# @Email   : 592190443@qq.com
# @File    : email_send.py
# @Software: PyCharm

from django.core.mail import send_mail

from random import Random
from user.models import EmailVerifyRecord
from mymooc.settings import EMAIL_FROM

#生成随机字符串

def random_str(random_length=8):
    str = ''
    # 生成字符串的可选字符串
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) -1  #实际下标的长度
    random = Random()

    for i in range(random_length):
        str += chars[random.randint(0,length)] #随机取出字符

    return str


# 发送注册邮件
def send_email(email,send_type='register'):
    #发送之前先保存到数据库，到时候查询连接是否存在

    #实例化一个EmailVerifyRecord 对象
    email_record = EmailVerifyRecord()
    #生成随机的code放入链接
    code = random_str(16)

    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type

    email_record.save()

    #定义邮箱内容
    email_title = ""
    email_body = ""

    if send_type == 'register':  #如果发送类型为注册
        email_title = "慕学注册激活链接"
        email_body = "请点击下面的链接激活您的账号：http://127.0.0.1:8000/active/{0}".format(code)

        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，发件人邮箱地址，收件人（是一个字符串列表）
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status: #如果发送成功
            pass

    elif send_type == 'forget':
        email_title = "慕学找回密码链接"
        email_body = "请点击下面的链接找回您的密码：http://127.0.0.1:8000/reset/{0}".format(code)
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status:
            pass

    elif send_type == 'update_email':  #如果发送类型为重置邮箱
        email_title = "慕学邮箱修改链接"
        email_body = "请点击下面的链接修改您的邮箱：http://127.0.0.1:8000/reset/{0}".format(code)

        # 使用Django内置函数完成邮件发送。四个参数：主题，邮件内容，发件人邮箱地址，收件人（是一个字符串列表）
        send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
        if send_status: #如果发送成功
            pass


