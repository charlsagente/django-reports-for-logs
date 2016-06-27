# -*- coding: utf-8 -*-
import StringIO
from django.shortcuts import render
import json

# Create your views here.
from django.http import HttpResponse
from django.template import loader
import os
from parser.Statistics import Statistics
from wsgiref.util import FileWrapper
from parser.InputsHandler import InputsHandler

def index(request):
    return render(request, 'logmanagement/layout.html')


def tomcat_logs(request):
    return render(request, 'logmanagement/layout.html')


def rest(request):
    return render(request, 'logmanagement/layout.html')


def vista_1(request,start_date,end_date):

    stats=Statistics(start_date,end_date)
    data=stats.count_logs_by_log_level()
    return HttpResponse(json.dumps(data), content_type='application/json')


def get_log(request, folder,log_file):
    file_handler=InputsHandler()
    HttpResponse((), content_type='text/plain')
    response = HttpResponse(content=file_handler.get_file_contents(folder,log_file))
    response['Content-Type'] = 'text/plain'
    return response