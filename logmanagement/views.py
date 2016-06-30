# -*- coding: utf-8 -*-
import json

from django.shortcuts import render


# Create your views here.
from django.http import HttpResponse
from logmanagement.parser.logs_parsers.MwParser.MwStatistics import MwStatistics
from logmanagement.parser.logs_parsers.TomcatParser.TomcatStatistics import TomcatStatistics
from logmanagement.parser.logs_parsers.MwRest.MwRestStatistics import MwRestStatistics
from parser.InputsHandler import InputsHandler

def index(request):
    return render(request, 'logmanagement/layout.html')


def tomcat_logs(request):
    return render(request, 'logmanagement/layout.html')


def rest(request):
    return render(request, 'logmanagement/layout.html')


def get_json_mw_stats(request,start_date,end_date):

    stats=MwStatistics(start_date,end_date)
    data=stats.count_logs_by_log_level()
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_json_tomcat_stats(request,start_date,end_date):
    stats=TomcatStatistics(start_date,end_date)
    data=stats.count_logs_by_log_level()
    return HttpResponse(json.dumps(data), content_type='application/json')

def get_json_rest_stats(request,start_date,end_date):
    stats = MwRestStatistics(start_date,end_date)
    data=stats.count_logs_by_log_level()
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_log(request, folder,log_file):
    file_handler=InputsHandler()
    HttpResponse((), content_type='text/plain')
    response = HttpResponse(content=file_handler.get_file_contents(folder,log_file))
    response['Content-Type'] = 'text/plain'
    return response