from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
import celery.bin.amqp
import sys
import time
import socket
from socket import *
import json


# set the default Django settings module for the 'celery' program.
# os.chdir('E:/workspace/mcuWeb/mcuWeb')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mcuWeb.settings')
from django.conf import settings
# from system.models import *

app = Celery('mcuWeb', backend='rpc://', broker='pyamqp://')
app.conf.result_backend = 'rpc://'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_RESULT_SERIALIZER = ['json']
CELERY_TASK_SERIALIZER = ['json']
app.conf.beat_schedule = {
    'checkNet-every-10-seconds': {
        'task': 'mcuWeb.celery.checkNet',
        'schedule': 10.0,
    },
}
app.conf.timezone = 'UTC'

amqp = celery.bin.amqp.amqp(app = app)

#
# # Using a string here means the worker doesn't have to serialize
# # the configuration object to child processes.
# # - namespace='CELERY' means all celery-related configuration keys
# #   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')
#
# # Load task modules from all registered Django app configs.
app.autodiscover_tasks()

HOST = "127.0.0.1"
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

@app.task(bind=True)
def callallCeleryTask(self,meetName="",chairMan="",memberList=""):
    global tcpCliSock

    memberList = json.loads(memberList)
    print("callallTask task",memberList,type(memberList))
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        tcpCliSock.settimeout(3)
    try:
        for member in memberList:
            # first addmember
            # second setmemberavformatparaTask

            memberName = member['name']
            memberIP = member['terminalIP']
            capalityName = member['capalityName']
            msg = ("ADDMEMBER\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nMemberName:%s\r\nMemberIP:%s\r\nMemberE164Alias:%s\r\nMemberH232Alias:%s\r\n\r\n" \
                % (meetName,memberName,memberIP,memberName,memberName))

            tcpCliSock.send(msg.encode('utf8'))
            time.sleep(0.05)
            msg = ("SETMEMBERAVFORMATPARA\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nMemberName:%s\r\nCapabilityName:%s\r\n\r\n" \
                % (meetName,memberName,capalityName))

            tcpCliSock.send(msg.encode('utf8'))

            # if memberName == chairMan:
            #     print("-------------chairMan------------")
            #     time.sleep(0.05)
            #     msg = ("SETMEMBERIDENTITY\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\n\r\n" \
            #         % (1,meetName,memberName)).encode('utf8')
            #     tcpCliSock.send(msg)
        # third callall
        # optional setidentity
        time.sleep(0.1)
        msg = "CALLALL\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\n\r\n" % (meetName)
        tcpCliSock.send(msg.encode('utf8'))
        print("wait",len(memberList))
        time.sleep(len(memberList)+2)
        print("wait")
        msg = ("SETMEMBERIDENTITY\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\n\r\n" \
            % (1,meetName,chairMan)).encode('utf8')
        tcpCliSock.send(msg)

    except BaseException as e:
        print("BaseException: ",e)
        tcpCliSock = None


@app.task(bind=True)
def hungallCeleryTask(self,meetName="",memberList=""):
    global tcpCliSock

    memberList = json.loads(memberList)
    print("hungallCeleryTask task",memberList,type(memberList))
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        tcpCliSock.settimeout(3)
    try:
        msg = ("HUNGUPALL\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\n\r\n" \
            % (1,meetName)).encode('utf8')
        tcpCliSock.send(msg)
        time.sleep(0.5*len(memberList))
        for member in memberList:
            # first addmember
            # second setmemberavformatparaTask

            msg = ("DELETEMEMBER\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\n\r\n" \
                % (1,meetName,member)).encode('utf8')
            # print(msg)
            tcpCliSock.send(msg)
            time.sleep(0.1)
        return None

    except BaseException as e:
        print("BaseException: ",e)
        tcpCliSock = None




#
# def brokenpipeHandle():
#     pass
#
# def makeConnection():
#     global tcpCliSock
#     if tcpCliSock is not None:
#         tcpCliSock.close()
#     tcpCliSock = None
#     while tcpCliSock is None:
#         try:
#             tcpCliSock = socket(AF_INET,SOCK_STREAM)
#             tcpCliSock.connect(ADDR)
#             tcpCliSock.settimeout(3)
#         except BaseException as e:
#             tcpCliSock = None
#             print(e)
#             time.sleep(3)
#     return True
#
# # ------------------------------------------------------------------------------------------------------------------------------------------
#
# @app.task(bind=True)
# def debug_task(self):
#     print('Request: {0!r}'.format(self.request))
#
# @app.task(bind=True,time_limit=20, soft_time_limit=10)
# def testTask(self):
#     print("running task")
#     global tcpCliSock
#     global amqp
#     global app
#     if tcpCliSock is None:
#
#         print("tcpCliSock is None")
#         tcpCliSock = socket(AF_INET,SOCK_STREAM)
#         tcpCliSock.connect(ADDR)
#         tcpCliSock.settimeout(3)
#     print("hello celery && Django",tcpCliSock)
#     try:
#         tcpCliSock.send("LISTMEET\r\nVersion 1\r\nSeqNumber 1\r\n\r\n".encode('utf8'))
#         data=tcpCliSock.recv(BUFSIZ)
#         print(data)
#     # 开始连接成功，后来MCU断开连接了
#     except ConnectionResetError as e:
#         print("ConnectionResetError error: ",e)
#         makeConnection()
#         # print(amqp.run('queue.purge','celery'))
#         print(app.control.purge())
#         testTask()
#     # 没连接到MCU
#     except BrokenPipeError as e:
#         print("BrokenPipeError: ",e)
#         makeConnection()
#
#         testTask()
#     except IOError as e:
#         print("ioerror:",e)
#         return None
#     except BaseException as e:
#         print("BaseException: ",e)
#         makeConnection()
#
#         testTask()
#
# @app.task(bind=True,time_limit=20, soft_time_limit=10)
# def setmeetgeneraparaTask(self,meetName="",meetMode="0",meetType="0"):
#     print("running task")
#     global tcpCliSock
#     global amqp
#     global app
#     if tcpCliSock is None:
#         print("tcpCliSock is None")
#         tcpCliSock = socket(AF_INET,SOCK_STREAM)
#         tcpCliSock.connect(ADDR)
#         tcpCliSock.settimeout(3)
#     print("setmeetgenerapara task")
#     try:
#         tcpCliSock.send(("SETMEETGENERALPARA\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nMeetMode:%s\r\nMeetType:%s\r\n\r\n" % (meetName,meetMode,meetType)).encode('utf8'))
#         print((("SETMEETGENERAPARA\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nMeetMode:%s\r\nMeetType:%s\r\n\r\n" % (meetName,meetMode,meetType))))
#         data=tcpCliSock.recv(BUFSIZ)
#         print(data.decode("utf8"))
#         if data is not None:
#             return data.decode("utf8")
#         return None
#     # 开始连接成功，后来MCU断开连接了
#     except ConnectionResetError as e:
#         print("ConnectionResetError error: ",e)
#         makeConnection()
#     # 没连接到MCU
#     except BrokenPipeError as e:
#         print("BrokenPipeError: ",e)
#         makeConnection()
#     except IOError as e:
#         print("ioerror:",e)
#         return None
#     except BaseException as e:
#         print("BaseException: ",e)
#         makeConnection()
#
# @app.task(bind=True,time_limit=20, soft_time_limit=10)
# def addmeetTask(self,meetName="",meetAlias="",meetRemark=""):
#     global tcpCliSock
#     global amqp
#     global app
#     if meetName is "":
#         return "param error"
#     if tcpCliSock is None:
#
#         print("tcpCliSock is None")
#         tcpCliSock = socket(AF_INET,SOCK_STREAM)
#         tcpCliSock.connect(ADDR)
#         tcpCliSock.settimeout(3)
#     print("addmeetTask task")
#     try:
#         tcpCliSock.send(("ADDMEET\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nMeetAlias:%s\r\nMeetRemark:%s\r\n\r\n" % (meetName,meetAlias,meetRemark)).encode('utf8'))
#         data=tcpCliSock.recv(BUFSIZ)
#         if data is not None:
#             print(data.decode("utf8"))
#             return data.decode("utf8")
#         return None
#     # 开始连接成功，后来MCU断开连接了
#     except ConnectionResetError as e:
#         print("ConnectionResetError error: ",e)
#         makeConnection()
#         makeConnection()
#     # 没连接到MCU
#     except BrokenPipeError as e:
#         print("BrokenPipeError: ",e)
#         makeConnection()
#     except IOError as e:
#         print("ioerror:",e)
#         return None
#     except BaseException as e:
#         print("BaseException: ",e)
#         makeConnection()
#
# @app.task(bind=True,time_limit=20, soft_time_limit=10)
# def deletemeetTask(self,meetName=""):
#     global tcpCliSock
#     global amqp
#     global app
#     if tcpCliSock is None:
#         print("tcpCliSock is None")
#         tcpCliSock = socket(AF_INET,SOCK_STREAM)
#         tcpCliSock.connect(ADDR)
#         tcpCliSock.settimeout(3)
#     print("deletemeetTask task")
#     try:
#         tcpCliSock.send(("DELETEMEET\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\n\r\n" % meetName).encode('utf8'))
#         data=tcpCliSock.recv(BUFSIZ)
#         print(data)
#     # 开始连接成功，后来MCU断开连接了
#     except ConnectionResetError as e:
#         print("ConnectionResetError error: ",e)
#         # makeConnection()
#     # 没连接到MCU
#     except BrokenPipeError as e:
#         print("BrokenPipeError: ",e)
#         makeConnection()
#     except IOError as e:
#         print("ioerror:",e)
#     except BaseException as e:
#         print("BaseException: ",e)
#         # makeConnection()
#
#
# @app.task(bind=True,time_limit=20, soft_time_limit=10)
# def listmeetTask(self):
#     global tcpCliSock
#     global amqp
#     global app
#     print(app.current_worker_task)
#     if tcpCliSock is None:
#         print("tcpCliSock is None")
#         tcpCliSock = socket(AF_INET,SOCK_STREAM)
#         tcpCliSock.connect(ADDR)
#         tcpCliSock.settimeout(3)
#     print("listmeetTask task")
#     try:
#         tcpCliSock.send("LISTMEET\r\nVersion:1\r\nSeqNumber:110\r\n\r\n".encode('utf8'))
#         data=tcpCliSock.recv(BUFSIZ)
#         return data.decode("utf8")
#     # 开始连接成功，后来MCU断开连接了
#     except BaseException as e:
#         print("BaseException: ",e)
#         tcpCliSock = None
#
# @app.task(bind=True,time_limit=20, soft_time_limit=10)
# def addmemberTask(self,meetName="",memberName="0",memberIP="0"):
#     global tcpCliSock
#     if tcpCliSock is None:
#         print("tcpCliSock is None")
#         tcpCliSock = socket(AF_INET,SOCK_STREAM)
#         tcpCliSock.connect(ADDR)
#         tcpCliSock.settimeout(3)
#     print("addmemberTask task")
#     try:
#         msg = ("ADDMEMBER\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nMemberName:%s\r\nMemberIP:%s\r\nMemberE164Alias:%s\r\nMemberH232Alias:%s\r\n\r\n" \
#             % (meetName,memberName,memberIP,memberName,memberName))
#         print(msg)
#         tcpCliSock.send(msg.encode('utf8'))
#         data=tcpCliSock.recv(BUFSIZ)
#         print(data.decode("utf8"))
#         if data is not None:
#             return data.decode("utf8")
#         return None
#     # 开始连接成功，后来MCU断开连接了
#     except BaseException as e:
#         print("BaseException: ",e)
#         tcpCliSock = None
#         return None
#
# @app.task(bind=True,time_limit=20, soft_time_limit=10)
# def setmemberavformatparaTask(self,meetName="",memberName="0",capalityName="1080P"):
#     global tcpCliSock
#     if tcpCliSock is None:
#         print("tcpCliSock is None")
#         tcpCliSock = socket(AF_INET,SOCK_STREAM)
#         tcpCliSock.connect(ADDR)
#         tcpCliSock.settimeout(3)
#     print("addmemberTask task")
#     try:
#         msg = ("SETMEMBERAVFORMATPARA\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nMemberName:%s\r\nCapabilityName:%s\r\n\r\n" \
#             % (meetName,memberName,capalityName))
#         print(msg)
#         tcpCliSock.send(msg.encode('utf8'))
#         data=tcpCliSock.recv(BUFSIZ)
#         print(data.decode("utf8"))
#         if data is not None:
#             return data.decode("utf8")
#         return None
#     # 开始连接成功，后来MCU断开连接了
#     except BaseException as e:
#         print("BaseException: ",e)
#         tcpCliSock = None
#         return None
#
# @app.task(bind=True,time_limit=20, soft_time_limit=10)
# def callmemberTask(self,meetName="",memberName="0"):
#     global tcpCliSock
#     if tcpCliSock is None:
#         print("tcpCliSock is None")
#         tcpCliSock = socket(AF_INET,SOCK_STREAM)
#         tcpCliSock.connect(ADDR)
#         tcpCliSock.settimeout(3)
#     print("callmemberTask task")
#     try:
#         msg = ("CALLMEMBER\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nMemberName:%s\r\n\r\n" \
#             % (meetName,memberName))
#         print(msg)
#         tcpCliSock.send(msg.encode('utf8'))
#         data=tcpCliSock.recv(BUFSIZ)
#         print(data.decode("utf8"))
#         if data is  None:
#             return None
#         data=tcpCliSock.recv(BUFSIZ)
#         print(data.decode("utf8"))
#         # return data.decode("utf8")
#         return None
#     # 开始连接成功，后来MCU断开连接了
#     except BaseException as e:
#         print("callmemberTask BaseException: ",e)
#         tcpCliSock = None
#         return None
#
# @app.task
# def checkNet():
#     print("checkNet!")
#     global tcpCliSock
#     global seqNumber
#     seqNumber+=1
#     if tcpCliSock is not None:
#         try:
#             tcpCliSock.send(("HEARTBEAT\r\nVersion:1\r\nSeqNumber:%d\r\n\r\n" % seqNumber).encode('utf8'))
#             data=tcpCliSock.recv(BUFSIZ)
#             print(seqNumber,'-------',data)
#             if data:
#                 return data.decode("utf8")
#         except BaseException as e:
#             print("schedule error: ",e)
#             tcpCliSock.close()
#             tcpCliSock = socket(AF_INET,SOCK_STREAM)
#             tcpCliSock.connect(ADDR)
#             tcpCliSock.settimeout(3)
#             return "error"
#     else:
#         tcpCliSock = socket(AF_INET,SOCK_STREAM)
#         tcpCliSock.connect(ADDR)
#         tcpCliSock.settimeout(3)
#         return "error"
#
# @app.task(bind=True,time_limit=20, soft_time_limit=10)
# def addavformatpara(self,meetname='',capalityname='',callbandwidth='',audioprotocol='',videoprotocol='',videoformat='',videoframerate=60):
#     global tcpCliSock
#     if tcpCliSock is None:
#         print("tcpCliSock is None")
#         tcpCliSock = socket(AF_INET,SOCK_STREAM)
#         tcpCliSock.connect(ADDR)
#         tcpCliSock.settimeout(3)
#     print("addavformatpara task")
#     try:
#         msg = ("ADDAVFORMATPARA\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nCapabilityName:%s\r\nCallBandWidth:%s\r\nAudioProtocol:%s\r\nVideoProtocol:%s\r\nVideoFormat:%s\r\nVideoFrameRate:%d\r\n\r\n" \
#             % (meetname,capalityname,callbandwidth,audioprotocol,videoprotocol,videoformat,videoframerate)).encode('utf8')
#         tcpCliSock.send(msg)
#         data=tcpCliSock.recv(BUFSIZ)
#         return data.decode("utf8")
#     # 开始连接成功，后来MCU断开连接了
#     except BaseException as e:
#         print("BaseException: ",e)
#         tcpCliSock = None
#         return None
#
# @app.task(bind=True,time_limit=20, soft_time_limit=10)
# def setdualformatparaTask(self,meetname="",dualprotocol='',dualformat='',dualBandWidth=1024):
#     global tcpCliSock
#     if tcpCliSock is None:
#         print("tcpCliSock is None")
#         tcpCliSock = socket(AF_INET,SOCK_STREAM)
#         tcpCliSock.connect(ADDR)
#         tcpCliSock.settimeout(3)
#     print("setdualformatparaTask task")
#     try:
#         msg = ("SETDUALFORMATPARA\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nDualProtocol:%s\r\nDualFormat:%s\r\nDualBandWidth:%d\r\n\r\n" \
#             % (meetname,dualprotocol,dualformat,dualBandWidth)).encode('utf8')
#         tcpCliSock.send(msg)
#         data=tcpCliSock.recv(BUFSIZ)
#         return data.decode("utf8")
#     # 开始连接成功，后来MCU断开连接了
#     except BaseException as e:
#         print("setdualformatparaTask BaseException: ",e)
#         tcpCliSock = None
#         return None
#
# @app.task(bind=True,time_limit=20, soft_time_limit=10)
# def getmeetinfoTask(self,meetName=""):
#     global tcpCliSock
#     if tcpCliSock is None:
#         print("tcpCliSock is None")
#         tcpCliSock = socket(AF_INET,SOCK_STREAM)
#         tcpCliSock.connect(ADDR)
#         tcpCliSock.settimeout(3)
#     print("getmeetinfoTask task")
#     try:
#         msg = ("GETMEETINFO\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\n\r\n" \
#             % (meetName))
#         print(msg)
#         tcpCliSock.send(msg.encode('utf8'))
#         data=tcpCliSock.recv(BUFSIZ)
#         print(data.decode("utf8"))
#         if data is not None:
#             return data.decode("utf8")
#         return None
#     # 开始连接成功，后来MCU断开连接了
#     except BaseException as e:
#         print("getmeetinfoTask BaseException: ",e)
#         tcpCliSock = None
#         return None
