# -*- coding:utf-8 -*-

from django import forms
#
#
#
class LoginForm(forms.Form):
    username = forms.CharField(required=True)#字段必须要有，字符型
    password = forms.CharField(required=True)


#注册表单的验证
class RegisterForm(forms.Form):
    email = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=6)
#
#
#
#找回密码的表单
class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)

#
#
#密码修改
class ModifyPwdForm(forms.Form):
    password1 = forms.CharField(required=True,min_length=5)
    password2 = forms.CharField(required=True, min_length=5)