"""mymooc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path
from django.views.static import serve  #处理静态图片

from mymooc.settings import MEDIA_ROOT ,STATIC_ROOT#寻找系统图片路径
from user.views import *
from organization.views import *
import xadmin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('xadmin/',xadmin.site.urls),

    #静态文件，自行配置，不使用django的自动管理
    re_path('static/(?P<path>.*)',serve,{'document_root':STATIC_ROOT}),

    # 处理图片显示的url, 使用Django自带serve, 传入参数告诉它去哪个路径找，我们有配置好的路径MEDIAROOT
    re_path('media/(?P<path>.*)', serve, {'document_root': MEDIA_ROOT}),

    path('index/',IndexView.as_view(),name="index"),
    path('login/',LoginView.as_view(),name="login"),
    path('logout/',LogoutView.as_view(),name="logout"),
    path('register/',ResgisterView.as_view(),name="register"),
    path('captcha/', include('captcha.urls')),  #验证码

    re_path('active/(?P<active_code>.*)/',ActiveUserView.as_view(),name='user_active') ,#用户激活

    re_path('reset/(?P<reset_code>.*)/',ResetView.as_view(),name = 'reset_pwd'), #忘记密码邮箱激活

    path('forget/',ForgetpwdView.as_view(),name='forget'),

    path('modify/',ModifyPwdView.as_view(),name='modify'),

    #课程机构url配置,分发
    path('org/', include('organization.urls' , namespace='org')),  #使用命名空间防止重名

    #课程列表页
    path('course/', include('course.urls', namespace='course')),  # 使用命名空间防止重名

    #用户个人中心相关地址
    path('users/', include('user.urls' , namespace='users')),  #使用命名空间防止重名



]
#全局404页面配置函数
handler404 = 'user.views.pag_not_found'
#全局500页面配置
handler500 = 'user.views.page_error'
