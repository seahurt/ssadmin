from django.shortcuts import render,redirect
from django.http import HttpResponse
import subprocess
import os
# from . import smtpp
# Create your views here.

def ssdaemon(request,cmd):
    info=[]
    if cmd == "start":
        if os.path.exists('/var/run/shadowsocks.pid'):
            info.append('<H1>ss server is already running....</H1>')
            cmd = 'restart'
        res = ssrun(cmd,info)
        return HttpResponse(res)
        
    if cmd =="stop":
        if os.path.exists('/var/run/shadowsocks.pid')==False:
            return HttpResponse("<H1>The server is not running...<H1>")
        res = ssrun(cmd,info)
        return HttpResponse(res)
    if cmd =="restart":
        if not os.path.exists('/var/run/shadowsocks.pid'):
            info.append('<H1>SS server is not running...</>')
            cmd = 'start'
        res = ssrun(cmd,info)
        return HttpResponse(res)

def ssrun(cmd,info):
    # 执行重启，开启，关闭任务
    sscmd = "ssserver -c /root/ss/ss.json -d "+cmd
    output = subprocess.check_output(sscmd,shell=True,stderr=subprocess.STDOUT)

    info.append("<H1>Perfoming {cmd}...</H1>".format(cmd=cmd))
    
    info.append("<p>"+output.decode('utf-8')+"</p>")

    return ''.join(info)

def showstatus(request):
    if is_run():
        return HttpResponse('<H1>The server is running</H1>')
    else:
        return HttpResponse('<H1>The server is not running</H1>')
def is_run():
    if os.path.exists('/var/run/shadowsocks.pid'):
        return True
    else:
        return False
def ssclick(request):
    if request.method == 'POST':
        action = request.POST['action']
        print(action)
        info = ssrun(action,[])
        #return HttpResponse(info)
        return redirect('/sss/')
    else:
        if is_run():
            status="running"
        else:
            status="not running"
        context = {
                  'status':status
                }
        return render(request, 'ssdaemon/ssd.html',context=context)

