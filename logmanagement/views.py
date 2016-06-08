# -*- coding: utf-8 -*-
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from django.template import loader
import os

def index(request):

    return render(request, 'logmanagement/index.html')

def vista_1(request,start_date,end_date):
    response="vista 1 %s %s"
    return HttpResponse(response % (start_date , end_date))