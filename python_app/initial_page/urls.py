from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^template/$', views.hello_template, name='hello_template'),  # 追加する

]