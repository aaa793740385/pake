# _*_ encoding:utf-8 _*_
from random import Random
from django.core.mail import send_mail

#from message.models import EmailVerifyRecord
from djangostart.settings import EMAIL_FROM


# def random_str(randomlength = 9):
#     str = ''
#     chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
#     length = len(chars) - 1
#     random = Random()
#     for i in range(randomlength):
#         str += chars[random.randint(0,length)]
#     return str
#
#
# def send_register_email(email,send_type = "register"):
#     email_record = EmailVerifyRecord() #实例化
#     code = random_str(16)#生成长度为16的随机字符串
#     email_record.code = code
#     email_record.email = email
#     email_record.send_type = send_type
#     email_record.save()
#
#     #向用户发送邮件
#     email_title = ""
#     email_body = ""
#
#     if send_type == "register":#注册
#         email_title = "慕学在线网注册激活链接"
#         email_body = "请点击下面链接激活你的账号：http://127.0.0.1:8000/active/{0}".format(code)
#
#         send_status = send_mail(email_title,email_body,EMAIL_FROM,[email])
#         if send_status:
#             pass
#     elif send_type == "forget":
#         email_title = "慕学在线网注册密码重置链接"
#         email_body = "请点击下面链接重置你的密码：http://127.0.0.1:8000/reset/{0}".format(code)
#
#         send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
#         if send_status:
#             pass
#
#
#
#
