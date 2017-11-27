from __future__ import absolute_import, unicode_literals
from django.http import HttpResponse
from channels.handler import AsgiHandler
from channels.sessions import channel_session
import json
import time
import os

import sys
import time
import socket
from socket import *
import threading



from channels import Group
from channels.sessions import channel_session
from channels.auth import channel_session_user_from_http


def ws_message(message):
    # ASGI WebSocket packet-received and send-packet message types
    # both have a "text" key for their textual data.
    message.reply_channel.send({
        "text": message.content['text'],
    })
# Connected to websocket.connect
@channel_session_user_from_http
def ws_connect(message):
    print("connect",message.channel.name,message.reply_channel.name,message['path'],message.user)

    Group("notifications").add(message.reply_channel)
    if message['path'] == '/meetlist/':
        Group("meetlist").add(message.reply_channel)
    time.sleep(3)
    Group("notifications").send({'text':"hello"},immediately=True)
    Group("meetlist").send({'text':"meetlist"},immediately=True)
    # for i in [0]:
    #
    #     # Accept the connection request
    #     message.reply_channel.send({
    #         "text": "wnl",
    #     }, immediately=True)
    #     time.sleep(1)
    # print("hello!")

print("into views")








HOST = "127.0.0.1"
PORT = 5038
BUFSIZ = 10240
ADDR = (HOST,PORT)
tcpCliSock = None
seqNumber = 0
try:
    tcpCliSock = socket(AF_INET,SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    # tcpCliSock.settimeout(3)
except BaseException as e:
    tcpCliSock = None
    print(e)



def loop():
    global tcpCliSock
    while True:
        data=tcpCliSock.recv(BUFSIZ)
        print("loop recv:",data)
        if message['path'] == '/meetlist/':
            Group("meetlist").send({'text':data.decode('utf8')},immediately=True)
        Group("notifications").send({'text':data.decode('utf8')},immediately=True)
t = threading.Thread(target=loop)
t.start()

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

# ------------------------------------------------------------------------------------------------------------------------------------------

def testTask():
    print("running task")
    global tcpCliSock

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

def setmeetgeneraparaTask(meetName="",meetMode="0",meetType="0"):
    print("running task")
    global tcpCliSock
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        tcpCliSock.settimeout(3)
    print("setmeetgenerapara task")
    try:
        tcpCliSock.send(("SETMEETGENERALPARA\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nMeetMode:%s\r\nMeetType:%s\r\n\r\n" % (meetName,meetMode,meetType)).encode('utf8'))
        print((("SETMEETGENERAPARA\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nMeetMode:%s\r\nMeetType:%s\r\n\r\n" % (meetName,meetMode,meetType))))
    # 开始连接成功，后来MCU断开连接了
    except ConnectionResetError as e:
        print("ConnectionResetError error: ",e)
        # makeConnection()
    # 没连接到MCU
    except BrokenPipeError as e:
        print("BrokenPipeError: ",e)
        # makeConnection()
    except IOError as e:
        print("ioerror:",e)
        return None
    except BaseException as e:
        print("BaseException: ",e)
        # makeConnection()

def addmeetTask(meetName="",meetAlias="",meetRemark=""):
    global tcpCliSock
    if meetName is "":
        return "param error"
    if tcpCliSock is None:

        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        tcpCliSock.settimeout(3)
    print("addmeetTask task")
    try:
        tcpCliSock.send(("ADDMEET\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nMeetAlias:%s\r\nMeetRemark:%s\r\n\r\n" % (meetName,meetAlias,meetRemark)).encode('utf8'))
    # 开始连接成功，后来MCU断开连接了
    except ConnectionResetError as e:
        print("ConnectionResetError error: ",e)
        makeConnection()
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

def deletemeetTask(meetName=""):
    global tcpCliSock
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        tcpCliSock.settimeout(3)
    print("deletemeetTask task")
    try:
        tcpCliSock.send(("DELETEMEET\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\n\r\n" % meetName).encode('utf8'))

    # 开始连接成功，后来MCU断开连接了
    except ConnectionResetError as e:
        print("ConnectionResetError error: ",e)
        # makeConnection()
    # 没连接到MCU
    except BrokenPipeError as e:
        print("BrokenPipeError: ",e)
        makeConnection()
    except IOError as e:
        print("ioerror:",e)
    except BaseException as e:
        print("BaseException: ",e)
        # makeConnection()


def listmeetTask():
    global tcpCliSock
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        tcpCliSock.settimeout(3)
    print("listmeetTask task")
    try:
        tcpCliSock.send("LISTMEET\r\nVersion:1\r\nSeqNumber:110\r\n\r\n".encode('utf8'))

    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("BaseException: ",e)
        tcpCliSock = None

def addmemberTask(meetName="",memberName="0",memberIP="0"):
    global tcpCliSock
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        tcpCliSock.settimeout(3)
    print("addmemberTask task")
    try:
        msg = ("ADDMEMBER\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nMemberName:%s\r\nMemberIP:%s\r\nMemberE164Alias:%s\r\nMemberH232Alias:%s\r\n\r\n" \
            % (meetName,memberName,memberIP,memberName,memberName))
        print(msg)
        tcpCliSock.send(msg.encode('utf8'))

    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("BaseException: ",e)
        tcpCliSock = None
        return None

def setmemberavformatparaTask(meetName="",memberName="0",capalityName="1080P"):
    global tcpCliSock
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        tcpCliSock.settimeout(3)
    print("addmemberTask task")
    try:
        msg = ("SETMEMBERAVFORMATPARA\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nMemberName:%s\r\nCapabilityName:%s\r\n\r\n" \
            % (meetName,memberName,capalityName))
        print(msg)
        tcpCliSock.send(msg.encode('utf8'))

    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("BaseException: ",e)
        tcpCliSock = None
        return None

def callmemberTask(meetName="",memberName="0"):
    global tcpCliSock
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        tcpCliSock.settimeout(3)
    print("callmemberTask task")
    try:
        msg = ("CALLMEMBER\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nMemberName:%s\r\n\r\n" \
            % (meetName,memberName))
        print(msg)
        tcpCliSock.send(msg.encode('utf8'))

    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("callmemberTask BaseException: ",e)
        tcpCliSock = None
        return None

def checkNet():
    print("checkNet!")
    global tcpCliSock
    global seqNumber
    seqNumber+=1
    if tcpCliSock is not None:
        try:
            tcpCliSock.send(("HEARTBEAT\r\nVersion:1\r\nSeqNumber:%d\r\n\r\n" % seqNumber).encode('utf8'))

        except BaseException as e:
            print("schedule error: ",e)
            tcpCliSock.close()
            tcpCliSock = socket(AF_INET,SOCK_STREAM)
            tcpCliSock.connect(ADDR)
            tcpCliSock.settimeout(3)
            return "error"
    else:
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        tcpCliSock.settimeout(3)
        return "error"

def addavformatpara(meetname='',capalityname='',callbandwidth='',audioprotocol='',videoprotocol='',videoformat='',videoframerate=60):
    global tcpCliSock
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        tcpCliSock.settimeout(3)
    print("addavformatpara task")
    try:
        msg = ("ADDAVFORMATPARA\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nCapabilityName:%s\r\nCallBandWidth:%s\r\nAudioProtocol:%s\r\nVideoProtocol:%s\r\nVideoFormat:%s\r\nVideoFrameRate:%d\r\n\r\n" \
            % (meetname,capalityname,callbandwidth,audioprotocol,videoprotocol,videoformat,videoframerate)).encode('utf8')
        tcpCliSock.send(msg)

    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("BaseException: ",e)
        tcpCliSock = None
        return None

def setdualformatparaTask(meetname="",dualprotocol='',dualformat='',dualBandWidth=1024):
    global tcpCliSock
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        tcpCliSock.settimeout(3)
    print("setdualformatparaTask task")
    try:
        msg = ("SETDUALFORMATPARA\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nDualProtocol:%s\r\nDualFormat:%s\r\nDualBandWidth:%d\r\n\r\n" \
            % (meetname,dualprotocol,dualformat,dualBandWidth)).encode('utf8')
        tcpCliSock.send(msg)

    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("setdualformatparaTask BaseException: ",e)
        tcpCliSock = None
        return None

def getmeetinfoTask(meetName=""):
    global tcpCliSock
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)
        tcpCliSock.settimeout(3)
    print("getmeetinfoTask task")
    try:
        msg = ("GETMEETINFO\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\n\r\n" \
            % (meetName))
        print(msg)
        tcpCliSock.send(msg.encode('utf8'))

    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("getmeetinfoTask BaseException: ",e)
        tcpCliSock = None
        return None













# ------------------------------------------------------------------------
