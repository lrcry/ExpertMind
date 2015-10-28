from django.conf.urls import url
from . import views
from django.conf.urls import *
from django.contrib import admin
admin.autodiscover()

urlpatterns = [
    url(r'^$', views.index, name='index'),
]
