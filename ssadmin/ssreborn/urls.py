from django.conf.urls import url
from . import views

app_name = 'ssreborn'
urlpatterns = [
    url(r'^ssr/$',views.ssreborn,name='ssreborn'),
]
