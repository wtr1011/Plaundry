from django.shortcuts import render
from django.http.response import HttpResponse

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
    return render(request, 'init_end.html')