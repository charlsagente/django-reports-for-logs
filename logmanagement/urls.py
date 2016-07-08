__author__ = 'charls'

from django.conf.urls import url
from . import views

urlpatterns = [
    # ex: /monitoreo/
    url(r'^$', views.index, name='index'),
    url(r'^(?P<start_date>[0-9]{4}-[0-9]{2}-[0-9]{2})/(?P<end_date>[0-9]{4}-[0-9]{2}-[0-9]{2})/$', views.get_json_mw_stats, name='vista 1'),
    url(r'^tomcat/(?P<start_date>[0-9]{4}-[0-9]{2}-[0-9]{2})/(?P<end_date>[0-9]{4}-[0-9]{2}-[0-9]{2})/$', views.get_json_tomcat_stats, name='vista 1 tomcat'),
    url(r'^elastic/(?P<start_date>[0-9]{4}-[0-9]{2}-[0-9]{2})/(?P<end_date>[0-9]{4}-[0-9]{2}-[0-9]{2})/$', views.get_json_elastic_stats, name='ajax elastic'),
    url(r'^rest/(?P<start_date>[0-9]{4}-[0-9]{2}-[0-9]{2})/(?P<end_date>[0-9]{4}-[0-9]{2}-[0-9]{2})/$', views.get_json_rest_stats, name='vista rest'),
    #url(r'^(?P<folder>\w+)/(?P<log_file>.+\.log)', views.get_log, name='get_log'),
    url(r'tomcat/$', views.tomcat_logs, name='tomcat'),
    url(r'showlog/(?P<folder>\w+)/(?P<log_file>.+\.log)/(?P<lines>(\d{1,5}\,*)*)$', views.show_log, name='show_log'),
    url(r'rest/$', views.rest, name='rest'),
    url(r'elastic/$', views.elastic_search, name='elastic')


]
