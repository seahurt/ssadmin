#!python
from django.conf.urls import url
from . import views

app_name = 'ssdaemon'
urlpatterns = [
    url(r'^$',views.showstatus,name='show'),
    url(r'^ssd/(?P<cmd>restart|stop|start)/$',views.ssdaemon,name='ssd'),
    url(r'^sss/$',views.showstatus,name='show'),
    url(r'^ssd/$',views.ssclick,name='ssclick'),
]

