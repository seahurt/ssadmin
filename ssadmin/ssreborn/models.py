from django.db import models

# Create your models here.
class SSRecord(models.Model):
	SS_ENCODE_CHOICES = (
		('aes-256-cfb','aes-256-cfb'),
		('rc4-md5','rc4-md5'),
		('chacha20','chacha20'),
		('aes-256-gcm','aes-256-gcm'),
		('camellia-256-cfb','camellia-256-cfb'),
	)
	def __str__(self):
		return str(self.port )
	port = models.IntegerField(default=0)
	created_time = models.DateTimeField(auto_now=True)
	passwd = models.CharField(max_length=20,default='1234')
	encode = models.CharField(max_length=25,default='aes-256-cfb',choices=SS_ENCODE_CHOICES)
