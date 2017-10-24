from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import celery.bin.amqp
import sys
import time
import socket
from socket import *

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcuWeb.settings')

app = Celery('mcuWeb', backend='rpc://', broker='pyamqp://')
app.conf.result_backend = 'rpc://'

app.conf.beat_schedule = {
    'checkNet-every-10-seconds': {
        'task': 'mcuWeb.celery.checkNet',
        'schedule': 10.0,
    },
}
app.conf.timezone = 'UTC'

amqp = celery.bin.amqp.amqp(app = app)


HOST = "192.168.43.152"
PORT = 5038
BUFSIZ = 10240
ADDR = (HOST,PORT)
tcpCliSock = None 
try:
	tcpCliSock = socket(AF_INET,SOCK_STREAM)
	tcpCliSock.connect(ADDR)
	tcpCliSock.settimeout(3)
except BaseException as e:
	tcpCliSock = None 
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

def makeConnection():
	global tcpCliSock
	if tcpCliSock is not None:
		tcpCliSock.close()
	tcpCliSock = None
	while tcpCliSock is None:
		try:
			tcpCliSock = socket(AF_INET,SOCK_STREAM)
			tcpCliSock.connect(ADDR)
			tcpCliSock.settimeout(3)
		except BaseException as e:
			tcpCliSock = None 
			print(e)		
			time.sleep(3)
	return True


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

@app.task(bind=True,time_limit=20, soft_time_limit=10)
def testTask(self):
	print("running task")
	global tcpCliSock
	global amqp
	global app
	if tcpCliSock is None:

		print("tcpCliSock is None")
		tcpCliSock = socket(AF_INET,SOCK_STREAM)
		tcpCliSock.connect(ADDR)
		tcpCliSock.settimeout(3)	
	print("hello celery && Django",tcpCliSock)
	try:
		tcpCliSock.send("LISTMEET\r\nVersion 1\r\nSeqNumber 1\r\n\r\n".encode('utf8'))
		data=tcpCliSock.recv(BUFSIZ)
		print(data)
	# 开始连接成功，后来MCU断开连接了
	except ConnectionResetError as e:
		print("ConnectionResetError error: ",e)
		makeConnection()
		# print(amqp.run('queue.purge','celery'))
		print(app.control.purge())
		testTask()
	# 没连接到MCU
	except BrokenPipeError as e:
		print("BrokenPipeError: ",e)
		makeConnection()
		
		testTask()
	except IOError as e:
		print("ioerror:",e)
		return None
	except BaseException as e:
		print("BaseException: ",e)
		makeConnection()
		
		testTask()

@app.task(bind=True,time_limit=20, soft_time_limit=10)
def setmeetgeneraparaTask(self,meetName="",meetMode="0",meetType="0"):
	print("running task")
	global tcpCliSock
	global amqp
	global app
	if tcpCliSock is None:

		print("tcpCliSock is None")
		tcpCliSock = socket(AF_INET,SOCK_STREAM)
		tcpCliSock.connect(ADDR)
		tcpCliSock.settimeout(3)	
	print("setmeetgenerapara task")
	try:
		tcpCliSock.send(("SETMEETGENERALPARA\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nMeetMode:%s\r\nMeetType:%s\r\n\r\n" % (meetName,meetMode,meetType)).encode('utf8'))
		print((("SETMEETGENERAPARA\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nMeetMode:%s\r\nMeetType:%s\r\n\r\n" % (meetName,meetMode,meetType))))
		data=tcpCliSock.recv(BUFSIZ)
		print(data.decode("utf8"))
		if data is not None:
			return data.decode("utf8")
		return None
	# 开始连接成功，后来MCU断开连接了
	except ConnectionResetError as e:
		print("ConnectionResetError error: ",e)
		makeConnection()
	# 没连接到MCU
	except BrokenPipeError as e:
		print("BrokenPipeError: ",e)
		makeConnection()
	except IOError as e:
		print("ioerror:",e)
		return None
	except BaseException as e:
		print("BaseException: ",e)
		makeConnection()

@app.task(bind=True,time_limit=20, soft_time_limit=10)
def addmeetTask(self,meetName="",meetRemark=""):
	global tcpCliSock
	global amqp
	global app
	if meetName is "":
		return "param error"
	if tcpCliSock is None:

		print("tcpCliSock is None")
		tcpCliSock = socket(AF_INET,SOCK_STREAM)
		tcpCliSock.connect(ADDR)
		tcpCliSock.settimeout(3)	
	print("addmeetTask task")
	try:
		tcpCliSock.send(("ADDMEET\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nMeetAlias:0%s\r\nMeetRemark:%s\r\n\r\n" % (meetName,meetName,meetRemark)).encode('utf8'))
		data=tcpCliSock.recv(BUFSIZ)
		if data is not None:
			print(data.decode("utf8"))
			return data.decode("utf8")
		return None
	# 开始连接成功，后来MCU断开连接了
	except ConnectionResetError as e:
		print("ConnectionResetError error: ",e)
		makeConnection()
	# 没连接到MCU
	except BrokenPipeError as e:
		print("BrokenPipeError: ",e)
		makeConnection()
	except IOError as e:
		print("ioerror:",e)
		return None
	except BaseException as e:
		print("BaseException: ",e)
		makeConnection()

@app.task(bind=True,time_limit=20, soft_time_limit=10)
def deletemeetTask(self):
	global tcpCliSock
	global amqp
	global app
	if tcpCliSock is None:

		print("tcpCliSock is None")
		tcpCliSock = socket(AF_INET,SOCK_STREAM)
		tcpCliSock.connect(ADDR)
		tcpCliSock.settimeout(3)	
	print("deletemeetTask task")
	try:
		tcpCliSock.send("DELETEMEET\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:01020170011\r\n\r\n".encode('utf8'))
		data=tcpCliSock.recv(BUFSIZ)
		print(data)
	# 开始连接成功，后来MCU断开连接了
	except ConnectionResetError as e:
		print("ConnectionResetError error: ",e)
		makeConnection()
		# print(amqp.run('queue.purge','celery'))
		print(app.control.purge())
		testTask()
	# 没连接到MCU
	except BrokenPipeError as e:
		print("BrokenPipeError: ",e)
		makeConnection()
		
		testTask()
	except IOError as e:
		print("ioerror:",e)
		# makeConnection()
		# testTask()
	except BaseException as e:
		print("BaseException: ",e)
		makeConnection()
		
		testTask()


@app.task(bind=True,time_limit=20, soft_time_limit=10)
def listmeetTask(self):
	global tcpCliSock
	global amqp
	global app
	if tcpCliSock is None:

		print("tcpCliSock is None")
		tcpCliSock = socket(AF_INET,SOCK_STREAM)
		tcpCliSock.connect(ADDR)
		tcpCliSock.settimeout(3)	
	print("listmeetTask task")
	try:
		tcpCliSock.send("LISTMEET\r\nVersion:1\r\nSeqNumber:110\r\n\r\n".encode('utf8'))
		data=tcpCliSock.recv(BUFSIZ)
		return data.decode("utf8")
	# 开始连接成功，后来MCU断开连接了
	except ConnectionResetError as e:
		print("ConnectionResetError error: ",e)
		makeConnection()
	# 没连接到MCU
	except BrokenPipeError as e:
		print("BrokenPipeError: ",e)
		makeConnection()
	except IOError as e:
		print("ioerror:",e)
		# makeConnection()
		# testTask()
	except BaseException as e:
		print("BaseException: ",e)
		makeConnection()

@app.task
def checkNet():
	print("checkNet!")
	global tcpCliSock
	if tcpCliSock is not None:
		try:
			tcpCliSock.send("HEARTBEAT\r\nVersion:1\r\nSeqNumber:1\r\n\r\n".encode('utf8'))
			data=tcpCliSock.recv(BUFSIZ)
			print(data)
		except BaseException as e:
			print("schedule error: ",e)
			tcpCliSock.close()
			tcpCliSock = socket(AF_INET,SOCK_STREAM)
			tcpCliSock.connect(ADDR)
			tcpCliSock.settimeout(3)
	else:
		tcpCliSock = socket(AF_INET,SOCK_STREAM)
		tcpCliSock.connect(ADDR)
		tcpCliSock.settimeout(3)