# -*- coding: utf-8 -*-
# @Time    : 2018/4/20 18:33
# @Author  : Wei
# @Email   : 592190443@qq.com
# @File    : urls.py
# @Software: PyCharm
from django.urls import path,re_path


from .views import CourseListView,CourseDetailView,CourseInfoView,CourseCommentView,AddCommentsView,CoursePlayView


app_name = "course"

urlpatterns = [
    path('list/',CourseListView.as_view(),name = 'course_list'),

    re_path('detail/(?P<course_id>\d+)/$', CourseDetailView.as_view(),name = 'course_detail'),#从公开课跳转到课程详情

    re_path('info/(?P<course_id>\d+)/$', CourseInfoView.as_view(), name='course_info'),  # 从课程详情跳转到章节详情

    re_path('comment/(?P<course_id>\d+)/$', CourseCommentView.as_view(), name='course_comment'),  # 从章节详情跳转到课程评论

    path('addcomment/',AddCommentsView.as_view(),name = 'add_comment'), #提交评论的ajax请求

    re_path('play/(?P<vedio_id>\d+)/$', CoursePlayView.as_view(), name='course_play'),  # 从章节详情跳转视频播放

]