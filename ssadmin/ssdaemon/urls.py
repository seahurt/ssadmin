#!python
from django.conf.urls import url
from . import views

app_name = 'ssdaemon'
urlpatterns = [
    url(r'^ssd/(?P<cmd>restart|stop|start)/$',views.ssdaemon,name='ssd'),
    url(r'^ssd/$',views.showstatus,name='show'),
    url(r'^sss/$',views.ssclick,name='ssclick'),
]

