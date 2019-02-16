from django.core.management.base import BaseCommand
from sscontrol.models import *
import re
import sys


class Command(BaseCommand):
    help = 'Setup Server Data'

    methods = ['aes-128-cfb', 'aes-128-ofb', 'aes-192-cfb', 'aes-192-ofb', 'aes-256-cfb', 'aes-256-ofb',
               'cast5-cfb', 'cast5-ofb', 'chacha20', 'rc4-md5']

    def get_method_list(self):
        s = ''
        for index, value in enumerate(self.methods):
            s += f'[{index}] {value}\n'
        return s

    def step1(self):
        print('Step 1: Create Admin User...')
        os.system('python manage.py createsuperuser')

    def step2(self):
        print('Step 2: Create Shadowsocks Config...')
        server = ''
        port = ''
        method = ''
        password = ''
        while True:
            server = input('Server IP:')
            if re.match('^[\d]{1,3}.[\d]{1,3}.[\d]{1,3}.[\d]{1,3}', server) is None:
                continue
            for x in server.split('.'):
                if int(x) >= 255:
                    server = ''
                    print('IP address not valid!')
                    break
            else:
                break

        while True:
            port = input('Server Port [1000~65535]:')
            if re.match('^[\d]{4,5}$', port) is None:
                continue
            if int(port) > 65535:
                print('Port is not valid!')
                continue
            else:
                port = int(port)
                break

        while True:
            method_index = input('Select Method: \n' + self.get_method_list())
            try:
                method = self.methods[int(method_index)]
            except Exception as e:
                print(e)
            else:
                break

        while True:
            password = input('Input password:')
            if len(password.strip()) > 1:
                password = password.strip()
                break

        print('\nYour ss config is:\n' +
              f'    Server: {server}\n' +
              f'    Port: {port}\n' +
              f'    Method: {method}\n' +
              f'    Password: {password}'
              )
        ok = input('Continue?[Y/n]')
        if ok.strip() == '':
            ok = 'y'

        if ok.lower() == 'y':
            SSrecord.objects.create(server=server, password=password, method=method, port=port)
            sys.exit('Setup Done!')
        else:
            sys.exit('Abort!')

    def handle(self, *args, **options):
        if User.objects.filter(is_superuser=True).count() == 0:
            self.step1()

        if SSrecord.objects.count() == 0:
            self.step2()
