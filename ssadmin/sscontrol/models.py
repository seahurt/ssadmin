from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
import os
import signal
# Create your models here.

# SS crypto method
CRYPTO_METHODS = [
    ('aes-256-cfb', 'aes-256-cfb'),
    ('rc4-md5', 'rc4-md5'),
    ('chacha20', 'chacha20'),
    ('aes-256-gcm', 'aes-256-gcm'),
    ('camellia-256-cfb', 'camellia-256-cfb'),
],


class SSrecord(models.Model):
    server = models.GenericIPAddressField(default='0.0.0.0')
    port = models.PositiveIntegerField(default=8888, unique=True)
    method = models.CharField(max_length=32)
    password = models.CharField(max_length=32)
    timeout = models.IntegerField(default=300)
    fast_open = models.BooleanField(default=False)
    workers = models.IntegerField(default=1)
    create_time = models.DateTimeField(auto_now_add=True)

    # class Meta:
    #     ordering = ['-id']

    @property
    def cmds(self):
        cmd = f'ssserver -s {self.server} -p {self.port} -k {self.password} -m {self.method} -t {self.timeout} --workers {self.workers} '
        if self.fast_open:
            cmd = cmd + '--fast-open'
        cmd += f'--pid-file {settings.SSPIDFILE}'
        return cmd

    @property
    def pidfile(self):
        return settings.SSPIDFILE

    def getpid(self):
        if not os.path.exists(self.pidfile):
            return None
        with open(self.pidfile) as f:
            return int(f.read().strip())

    def start(self):
        self.stop()
        os.system(self.cmds + ' -d start')

    def stop(self):
        if self.getpid() is not None:
            try:
                os.kill(self.getpid(), signal.SIGTERM)
            except OSError:
                pass

    def restart(self):
        self.stop()
        self.start()

    @property
    def status(self):
        if self.getpid() is not None:
            try:
                os.kill(self.getpid(), 0)
            except OSError:
                os.remove(self.pidfile)
                return 'stopped'
            return 'running'
        else:
            return 'stopped'


class SystemRecord(models.Model):
    action = models.CharField(max_length=10, choices=settings.ACTIONS)
    time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
