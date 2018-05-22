# -*- coding: utf-8 -*-
# @Time    : 2018/4/25 22:45
# @Author  : Wei
# @Email   : 592190443@qq.com
# @File    : urls.py
# @Software: PyCharm

from django.urls import path,re_path
from user.views import UserInfoView,UploadImageView,PwdUpdateView,SendEmailCodeView,UpdateEmail,MyCourseView,MyMsgView,MyFavOrgView,MyFavCourseView,MyFavTeacherView



app_name = "users"

urlpatterns = [
    #用户信息
    path('info/',UserInfoView.as_view(),name='users_info'),
    #用户头像上传
    path('image/upload/',UploadImageView.as_view(),name='image_upload'),

    #用户个人中心修改密码
    path('update/pwd/', PwdUpdateView.as_view(), name='update_pwd'),

    #修改发送邮箱验证码
    path('sendemail_code/', SendEmailCodeView.as_view(), name='sendemail_code'),

    #修改邮箱
    path('updata_email/', UpdateEmail.as_view(), name='update_email'),

    #我的课程
    path('mycourse/',MyCourseView.as_view(),name = 'mycourse'),
    #我的消息
    path('mymessage/',MyMsgView.as_view(),name = 'mymessage'),
    #我的收藏
        #机构
        path('myfav/org',MyFavOrgView.as_view(),name = 'myfav_org'),
        #课程
        path('myfav/course',MyFavCourseView.as_view(),name = 'myfav_course'),
        #讲师
        path('myfav/teacher',MyFavTeacherView.as_view(),name = 'myfav_teacher'),


]