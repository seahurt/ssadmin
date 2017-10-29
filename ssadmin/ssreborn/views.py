from django.shortcuts import render,redirect
from .models import *
from .ssforms import SSForm 
from django.http import HttpResponse
import json
import os
import random
# Create your views here.

def ssreborn(request):
    if request.method == 'POST':
        form = SSForm(request.POST)

        if form.is_valid():
            newRecord =form.save(commit=False)
            #print(newRecord.port)
            if newRecord.port == 0:
                newRecord.port = random.randrange(1000,7900)
            if rebuild(newRecord):
                # firewall(newRecord.port)
                newRecord.save()
                return redirect('/ssr/')
            else:
                return HttpResponse("<H1>Rebuild not succeed!!</H1>")
        else:
            return HttpResponse("<H1>POST info error!</H1>")
    else:
        form = SSForm()
        current_record = SSRecord.objects.order_by('-created_time')[0]
        context = {
                    'form':form,
                    'current_record':current_record
        }
        return render(request,'ssreborn/ssr.html',context=context)

def rebuild(record):
    config = {}
    config['server_port']=record.port
    config['server']='0.0.0.0'
    config['password']=record.passwd 
    config['method']=record.encode
    ss_config = "/root/ss/ss.json"
    f = open(ss_config,'w')
    json.dump(config,f,indent=4)
    f.write('\n')
    f.close() 
    os.system('ssserver -d stop')
    status = os.system('ssserver -c /root/ss/ss.json -d start')
    if status == 0:
        firewall(record.port)
        return True
    else:
        print ("Non-zero exit code when start ss server")
        return False

def firewall(port):
    oldport = SSRecord.objects.order_by('-created_time')[0].port
    rm_oldport = "sed -i 's/-A INPUT -p tcp --dport {oldport} -j ACCEPT/#@/' /etc/iptables.test.rules".format(oldport=oldport)
    activate_newport = "sed -i 's/#@/-A INPUT -p tcp --dport {newport} -j ACCEPT/' /etc/iptables.test.rules".format(newport=port)
    #print(rm_oldport)
    #print(activate_newport)
    os.system(rm_oldport)
    os.system(activate_newport)
    os.system("iptables-restore < /etc/iptables.test.rules")
    os.system("iptables-save >/etc/iptables.up.rules")
    
