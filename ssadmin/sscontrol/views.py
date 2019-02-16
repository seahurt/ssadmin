from django.shortcuts import render, redirect
from .models import *
import os
from django.contrib.auth.decorators import login_required
from random import randint
from django.contrib.auth import authenticate, login
# Create your views here.


class Message(object):
    msg = None
    type = None
    reason = None

    def __init__(self, msg=None, mtype=None, reason=None):
        self.msg = msg
        self.type = mtype
        self.reason = reason


@login_required()
def home(request):
    if request.method == 'GET':
        ssrecord = SSrecord.objects.order_by('-id').first()
        return render(request, 'index.html', context={'ssrecord': ssrecord})
    elif request.method == 'POST':
        action = request.POST.get('action')
        record = request.POST.get('record',  SSrecord.objects.order_by('-id').first().id)
        ssrecord = SSrecord.objects.get(pk=record)
        if action == 'start':
            ssrecord.start()
        elif action == 'stop':
            ssrecord.stop()
        elif action == 'restart':
            ssrecord.restart()
        return render(request, 'index.html', context={'ssrecord': ssrecord})


@login_required()
def history(request):
    return render(request, 'history.html', context={'records': SSrecord.objects.order_by('-d')[:10]})


@login_required()
def random(request):
    if request.method == 'GET':
        return render(request, 'random.html')
    elif request.method == 'POST':
        record = request.POST.get('record', SSrecord.objects.order_by('-id').first().id)
        ssrecord = SSrecord.objects.get(pk=record)
        ssrecord.port = randint(1080, 65000)
        ssrecord.save()
        ssrecord.start()
        return redirect('/home')


@login_required()
def rebuild(request):
    if request.method == 'GET':
        return render(request, 'rebuild.html')
    elif request.method == 'POST':
        ssid = request.POST.get('record', SSrecord.objects.order_by('-id').first().id)
        port = request.POST.get('port')
        method = request.POST.get('method')
        password = request.POST.get('password')
        ssrecord = SSrecord.objects.get(id=ssid)
        ssrecord.port = port
        ssrecord.method = method
        ssrecord.password = password
        ssrecord.save()
        ssrecord.start()
        return redirect('/home')
