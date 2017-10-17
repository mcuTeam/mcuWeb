from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import sys
import time
import socket
from socket import *

HOST = "192.168.43.152"
PORT = 5038
BUFSIZ = 1024
ADDR = (HOST,PORT)
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcuWeb.settings')

app = Celery('mcuWeb', backend='rpc://', broker='pyamqp://')
app.conf.result_backend = 'rpc://'

tcpCliSock = None 
try:
	tcpCliSock = socket(AF_INET,SOCK_STREAM)
	tcpCliSock.connect(ADDR)
	tcpCliSock.settimeout(3)
except BaseException as e:
	print(e)

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

def brokenpipeHandle():
	pass


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.task(bind=True)
def testTask(self):
	global tcpCliSock
	if tcpCliSock is None:
		tcpCliSock = socket(AF_INET,SOCK_STREAM)
		tcpCliSock.connect(ADDR)
		tcpCliSock.settimeout(3)	
	print("hello celery && Django")
	try:
		tcpCliSock.send("LISTMEET\r\nVersion 1\r\nSeqNumber 1\r\n\r\n".encode('utf8'))
		data=tcpCliSock.recv(BUFSIZ)
		print(data)
	except socket.error as e:
		print("socket error: "+e)
	except IOError as e:
		print("ioerror:"+e)
		tcpCliSock.close()
		tcpCliSock.connect(ADDR)
		tcpCliSock.settimeout(3)
	except BaseException as e:
		print(e)

@app.task(bind=True)
def makeTcp(self):
	pass
