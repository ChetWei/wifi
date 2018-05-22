# -*- coding: utf-8 -*-
# @Time    : 2018/4/18 19:25
# @Author  : Wei
# @Email   : 592190443@qq.com
# @File    : forms.py
# @Software: PyCharm

from django import forms

from captcha.fields import CaptchaField
from user.models import UserProfile



class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True,min_length=6)


class RegisterForm(forms.Form):
    email = forms.EmailField(required=True)
    password = forms.CharField(required=True,min_length=6)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


class ForgetForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={'invalid': '验证码错误'})


    '''重置密码'''
class ModifyPwdForm(forms.Form):

    password1 = forms.CharField(required=True, min_length=5)
    password2 = forms.CharField(required=True, min_length=5)



'''图片上传'''
class UploadImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['image']


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['nick_name','gender','birthday','adress','mobile']