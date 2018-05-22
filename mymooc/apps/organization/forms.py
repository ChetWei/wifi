# -*- coding: utf-8 -*-
# @Time    : 2018/4/19 10:57
# @Author  : Wei
# @Email   : 592190443@qq.com
# @File    : forms.py
# @Software: PyCharm
from django import forms

from operation.models import UserAsk
import re



'''直接将model转为form验证'''

class UserAskForm(forms.ModelForm):
    class Meta:
        model = UserAsk  #要转换的model
        fields = ['name','mobile','course_name']   #需要转换的字段

    '''验证手机号码字段是否合格必须规范名称'''

    def clean_mobile(self):
        mobile = self.cleaned_data['mobile']   #要验证的字段

        REGEX_MOBILE = re.compile('^1(3[0-9]|5[0-35-9]|8[025-9])\\d{8}$')
        if REGEX_MOBILE.match(mobile):
            return mobile
        else:
            raise forms.ValidationError('手机号码非法',code='mobile_invalid')

