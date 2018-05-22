# -*- coding: utf-8 -*-
# @Time    : 2018/4/23 12:34
# @Author  : Wei
# @Email   : 592190443@qq.com
# @File    : mixin_utils.py
# @Software: PyCharm


from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

class LoginRequiredMixin(object):
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self,request,*args,**kwargs):
        return super(LoginRequiredMixin, self).dispatch(request,*args,**kwargs)