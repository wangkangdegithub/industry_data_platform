from django.conf.urls import url
from .import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^indexs$',views.index),
    url(r'^charts$',views.charts),
    url(r'^blank$',views.blank),
    url(r'^cards$', views.cards),
    url(r'^forgotpassword$', views.forgotpassword),
    url(r'^login$', views.login),
    url(r'^navbar$', views.navbar),
    url(r'^register$', views.register),
    url(r'^tables$', views.tables),

]