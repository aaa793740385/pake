# -*- coding:utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.


class UserInformation(models.Model):
    true_name = models.CharField(max_length=32, default='天地一号')
    content = models.TextField(max_length=100, default='这个人很懒，什么都没留下~~~')
    sex = models.CharField(max_length=10, default='女')
    image = models.CharField(max_length=100, default='image/girl.jpg')
    crawl_time = models.CharField(max_length=100, default='0')

    def __unicode__(self):
        return self.true_name
    pass


class Task(models.Model):
    user = models.IntegerField(null=False)
    name = models.CharField(max_length=32, default='爬虫任务')
    general = models.CharField(max_length=32,null=False)
    remark = models.TextField(null=True)
    time = models.CharField(max_length=32, null=True)

    def __unicode__(self):
        return self.name
    pass


class Feedback(models.Model):
    content = models.TextField(null=False)
    pass



# class UserProfile(AbstractUser):
#     class Meta:
#         verbose_name = u"用户信息"
#         verbose_name_plural = verbose_name
#
#     def __unicode__(self):
#         return self.username
#
# class EmailVerifyRecord(models.Model):
#     code = models.CharField(max_length=20 , verbose_name=u"验证码")
#     email = models.EmailField(max_length=50 , verbose_name=u"邮箱")
#     send_type = models.CharField(verbose_name=u"验证码类型",choices=(("register", u"注册"),("forget" , "找回密码")) , max_length=10)
#     send_time = models.DateTimeField(verbose_name=u"发送时间",default=datetime.now)
#
#     class Meta:
#         verbose_name = u"邮箱验证码"
#         verbose_name_plural = verbose_name
#     #改写输出的验证码的名字，改写输出，要重载这个方法，不然就输出该名字
#     def __unicode__(self):
#         return '{0}({1})'.format(self.code,self.email)
