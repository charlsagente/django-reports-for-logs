__author__ = 'charls'

from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /logs/
    url(r'^$', views.index, name='index'),
    url(r'^(?P<start_date>[0-9]{4}-[0-9]{2}-[0-9]{2})/(?P<end_date>[0-9]{4}-[0-9]{2}-[0-9]{2})/$', views.vista_1, name='vista 1')
]