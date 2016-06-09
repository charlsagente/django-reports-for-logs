# -*- coding: utf-8 -*-
from django.shortcuts import render
import json

# Create your views here.
from django.http import HttpResponse
from django.template import loader
import os
from parser.Statistics import Statistics

def index(request):

    return render(request, 'logmanagement/index.html')

def vista_1(request,start_date,end_date):

    stats=Statistics()
    data=stats.count_logs_by_log_level(start_date,end_date)
    return HttpResponse(json.dumps(data), content_type='application/json')