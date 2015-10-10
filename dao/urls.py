__author__ = 'YUN'
from django.conf.urls import url

from . import views

urlpatterns = [
    # ex: /polls/
    url(r'^$', views.index, name='index'),
    # # ex: /polls/5/
    # url(r'^(?P<question_id>[0-9]+)/$', views.detail, name='detail'),
    # # ex: /polls/5/results/
    # url(r'^(?P<question_id>[0-9]+)/results/$', views.results, name='results'),
    # # ex: /polls/5/vote/
    # url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    #
    # # ex: /polls/result/5
    # url(r'^result/(?P<question_id>[a-zA-Z]+)/$', views.test, name='test'),
    #
    #
    # user register
    url(r'^user_register/(?P<user_name>[a-zA-Z]+)/$', views.user_register, name='user_register'),

]