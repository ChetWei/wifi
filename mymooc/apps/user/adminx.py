# -*- coding: utf-8 -*-
# @Time    : 2018/4/15 9:26
# @Author  : Wei
# @Email   : 592190443@qq.com
# @File    : adminx.py.py
# @Software: PyCharm
import xadmin
from xadmin import views  #全局配置
from .models import UserProfile,EmailVerifyRecord,Banner,LoginBanner


class EmailVerifyRecordAdmin(object):
    list_display = ['code', 'email', 'send_type', 'send_time']
    # 搜索的字段，不要添加时间搜索
    search_fields = ['code', 'email', 'send_type']
    # 过滤
    list_filter = ['code', 'email', 'send_type', 'send_time']
    
class BannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']


class LoginBannerAdmin(object):
    list_display = ['title', 'image', 'url', 'index', 'add_time']
    search_fields = ['title', 'image', 'url', 'index']
    list_filter = ['title', 'image', 'url', 'index', 'add_time']





xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(LoginBanner,LoginBannerAdmin)





#---------------全局配置----------------------



# 创建xadmin的最基本管理器配置，并与view绑定

class BaseSetting(object):
    # 开启主题功能
    enable_themes = True
    use_bootswatch = True

# 将基本配置管理与view绑定
xadmin.site.register(views.BaseAdminView,BaseSetting)


#全局修改，固定写法
class GlobalSettings(object):
    #修改右上角title
    site_title = "慕学后台管理"

    #修改footer
    site_footer = '魏名安'

    #收起菜单
    menu_style = 'accordion'

xadmin.site.register(views.CommAdminView,GlobalSettings)
