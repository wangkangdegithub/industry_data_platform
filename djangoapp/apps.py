from django.apps import AppConfig

#左侧app中文名称定义和多表紧缩
class DjangoappConfig(AppConfig):
    name = 'djangoapp'
    verbose_name = u'报表管理'