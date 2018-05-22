# -*- coding: utf-8 -*-
# @Time    : 2018/4/19 11:11
# @Author  : Wei
# @Email   : 592190443@qq.com
# @File    : urls.py
# @Software: PyCharm
from django.urls import path,re_path


from .views import OrgView,UserAskView,OrgHomeView,OrgCourseView,OrgTeacherView,OrgDescView,AddFavView,TeacherListView,TeacherDetail


app_name = "organization"
urlpatterns = [

    # 课程组织结构
    path('list/', OrgView.as_view(),name='org_list'), #组织结构首页

    path('user_ask/',UserAskView.as_view(),name='user_ask'),  #用户咨询ajax请求处理

    re_path('^home/(?P<org_id>\d+)$', OrgHomeView.as_view(), name="org_home"),    #处理从机构列表页到机构主页的url

    re_path('^course/(?P<org_id>\d+)$', OrgCourseView.as_view(), name="org_course"), #机构主页到课程页

    re_path('teacher/(?P<org_id>\d+)$', OrgTeacherView.as_view(), name="org_teacher"), #机构主页到老师详情页

    re_path('^desc/(?P<org_id>\d+)$', OrgDescView.as_view(), name="org_desc"), #机构主页到机构详情页

    path('add_fav/',AddFavView.as_view(),name = "add_fav"),                 #处理点赞ajax请求

    #讲师
    path('teacher/list/', TeacherListView.as_view(), name="teacher_list"),  # 讲师列表页
    re_path('teacher/detail/(?P<teacher_id>\d+)$', TeacherDetail.as_view(), name="teacher_detail"),  # 讲师详情页



]