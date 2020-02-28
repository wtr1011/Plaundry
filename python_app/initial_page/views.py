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
    #postnumber="2591292"
    #graph_save()
    time_sep_and_draw_graph(postnumber,"./static/")
    print(postnumber)
    return render(request, 'usual.html')


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
    #スクレイピングのデータとdatabaseのデータより提案の処理、グラフをpng変換
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
    #スクレイピングのデータとdatabaseのデータより提案の処理、グラフをpng変換

    executeCreateTable(postnumber)
    d = {
        'mon_plan':["8:00 ~ 9:00", "9:00 ~ 10:00"],
        'tue_plan':["11:00 ~ 14:00"],
        'wed_plan':["8:00 ~ 9:00", "9:00 ~ 10:00", "11:00 ~ 12:00"],
        'thr_plan':["8:00 ~ 9:00"],
        'fri_plan':["8:00 ~ 9:00", "9:00 ~ 10:00", "16:00 ~ 17:00", "20:00 ~ 21:00", "22:00 ~ 24:00"],
        'sat_plan':["8:00 ~ 9:00", "10:00 ~ 11:00"],
        'sun_plan':["8:00 ~ 24:00"],
    }
    return render(request, 'week_plan.html')



def graph_save():
    # y = f(x)
    x = np.linspace(-np.pi, np.pi)
    y1 = np.sin(x)+np.cos(x/2) 
    y2 = np.cos(x)+np.cos(x)

# figure
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

# plot
    ax.plot(x, y1, linestyle='--', color='b', label='y = sin(x)')
    ax.plot(x, y2, linestyle='-', color='#e46409', label='y = cos(x)')

# x axis
    plt.xlim([-np.pi, np.pi])
    ax.set_xticks([-np.pi, -np.pi/2, 0, np.pi/2, np.pi])
    ax.set_xticklabels(['-pi', '-pi/2', '0', 'pi/2', 'pi'])
    ax.set_xlabel('x')

# y axis
    plt.ylim([-1.2, 1.2])
    ax.set_yticks([-1, -0.5, 0, 0.5, 1])
    ax.set_ylabel('y')

# legend and title
    ax.legend(loc='best')
    ax.set_title('Plot of sine and cosine')


#スクレイピングのデータとdatabaseのデータより提案の処理、グラフをpng変換
# save as png
    plt.savefig('./static/figure.png')
    plt.clf()