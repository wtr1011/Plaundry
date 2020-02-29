from django.shortcuts import render,redirect
from django.http.response import HttpResponse
from . import forms, models
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from initial_page.python import result_day
from initial_page.python.draw_graph import time_sep_and_draw_graph
from initial_page.python.weekly_suggest_tb import executeCreateTable
from initial_page.python.pick_data import picker

#グローバル変数でデータ保存
postnumber=0
starttime=0
endtime=0
scale=0

# Create your views here.
#start page
def hello_template(request):
    return render(request, 'init_start.html')

#get post number
def get_post_query(request):
    d = {
        'your_postnumber': request.GET.get('your_postnumber')
    }
    return render(request, 'init_postnumber.html', d)


#get work time

def get_worktime(request):
    d = {
        'worktime_start': request.GET.get('worktime_start'),
        'worktime_end': request.GET.get('worktime_end')
    }
    return render(request, 'init_worktime.html', d)

#get laundry scale
def get_laundryscale(request):
    d = {
        'scale': request.GET.get('scale')
    }
    return render(request, 'init_laundryscale.html', d)


#end setting
def init_end_page(request):
    global postnumber, starttime, endtime, scale
    userData = request.GET.get("sendJSON", None)
    if "sendJSON" in request.GET:
        userData = userData.strip('"').split(',')
        postnumber = userData[0]
        starttime = userData[1]
        endtime = userData[2]
        scale = userData[3]

    return render(request, 'init_end.html')


#usual
def usual_page(request):
    global postnumber, starttime, endtime, scale
    userData = request.GET.get("sendJSON", None)
    if "sendJSON" in request.GET:
        userData = userData.strip('"').split(',')
        postnumber = userData[0]
        starttime = userData[1]
        endtime = userData[2]
        scale = userData[3]
    time_sep_and_draw_graph(postnumber,"./static/")

    instdata = picker()

    d = {
        'userID':instdata[0],
        'time':instdata[1],
        'height':instdata[2]*100,
        'weight':instdata[3]
    }

    return render(request, 'usual.html', d)


#plan today page
def today_plan(request):
    global postnumber, starttime, endtime, scale
    userData = request.GET.get("sendJSON", None)
    if "sendJSON" in request.GET:
        userData = userData.strip('"').split(',')
        postnumber = userData[0]
        starttime = userData[1]
        endtime = userData[2]
        scale = userData[3]

    time = result_day.output_time(postnumber)

    d = {
        'time':time,
        'num':postnumber
    }
    return render(request, 'today_plan.html',d)

#plan week page
def weekly_plan(request):
    global postnumber, starttime, endtime, scale
    userData = request.GET.get("sendJSON", None)
    if "sendJSON" in request.GET:
        userData = userData.strip('"').split(',')
        postnumber = userData[0]
        starttime = userData[1]
        endtime = userData[2]
        scale = userData[3]

    rank3 = executeCreateTable(postnumber, starttime, endtime)
    d = {
        '1st_plan_date':rank3[0][1][0],
        '1st_plan_time':rank3[0][1][1],
        '2nd_plan_date':rank3[1][1][0],
        '2nd_plan_time':rank3[1][1][1],
        '3rd_plan_date':rank3[2][1][0],
        '3rd_plan_time':rank3[2][1][1],
    }
    return render(request, 'week_plan.html', d)

