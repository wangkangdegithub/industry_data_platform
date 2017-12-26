"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from djangoapp.views import upload
from djangoapp.views import result
from djangoapp.views import homepage,index,charts,tables,navbar,cards,blank,forgotpassword,login
import xadmin

urlpatterns = [
    #url(r'^admin/', admin.site.urls),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^homepage/', homepage),
    url(r'^dashboard/', index),
    url(r'^dashboard/index', index),
    url(r'^dashboard/charts', charts),
    url(r'^dashboard/tables', tables),
    url(r'^dashboard/cards', cards),
    url(r'^dashboard/navbar', navbar),
    url(r'^dashboard/blank', blank),
    url(r'^dashboard/forgotpassword', forgotpassword),
    url(r'^dashboard/login', login),
    url(r'^upload/', upload),
    url(r'^result/', result),
]