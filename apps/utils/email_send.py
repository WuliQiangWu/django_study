# _*_ coding:utf-8 _*_
# __author__ : 'aj'
# __date__ : '2017/12/19 下午4:24'
from random import Random

from users.models import EmailVerifyRecord
from django.core.mail import send_mail
from whatFuck.settings import EMAIL_FROM


def random_str(randomlength=8):
    str = ''
    chars = 'QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm1234567890'
    lenth = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, lenth)]
    return str


def send_register_email(email, send_type='register'):
    email_record = EmailVerifyRecord()
    if send_type == 'email_update':
        code = random_str(4)
    else:
        code = random_str(16)
    email_record.code = code
    email_record.email = email
    email_record.send_type = send_type
    email_record.save()

    email_title = ''
    email_body = ''
    if send_type == 'register':
        email_title = '暮雪在线激活链接'
        email_body = '请点击下面链接激活你的账号： http://127.0.0.1:8000/active/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
    elif send_type == 'forget':
        email_title = '暮雪在线重置密码链接'
        email_body = '请点击下面链接重置你的密码： http://127.0.0.1:8000/reset/{0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass

    elif send_type == 'email_update':
        email_title = '暮雪在线修改邮箱验证码'
        email_body = '邮箱验证码为： {0}'.format(code)
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if send_status:
            pass
