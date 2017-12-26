import xadmin
from .models import NewTable
from xadmin import views
from django.apps import AppConfig

class NewTableAdmin(object):
    list_display = ['Datetime','Path','Tag','RenamePath']
    search_fields = ['Datetime','Path','Tag','RenamePath']
    list_filter = ['Datetime','Path','Tag','RenamePath']

xadmin.site.register(NewTable,NewTableAdmin)

# 主题设置
class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True

xadmin.site.register(views.BaseAdminView, BaseSetting)

# 页头页尾设置
class GlobalSetting(object):
    site_title = "工业大数据智慧平台管理系统"
    site_footer = "http://www.wangkang.link"

xadmin.site.register(views.CommAdminView, GlobalSetting)
