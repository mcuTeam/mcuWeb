from __future__ import absolute_import, unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse,HttpResponseServerError
import threading
from threading import Lock
import json

from fun.forms import *
from system.models import *
from system.views import *
import re
from django.core.cache import cache
# Create your views here.




import os

import sys
import time
import socket
from socket import *


HOST = "127.0.0.1"
PORT = 5038
BUFSIZ = 10240
ADDR = (HOST,PORT)
tcpCliSock = None
seqNumber = 0
recvDict={}
lock = Lock()

try:
    tcpCliSock = socket(AF_INET,SOCK_STREAM)
    tcpCliSock.connect(ADDR)

except BaseException as e:
    tcpCliSock = None


def loop():
    global tcpCliSock

    while True:
        try:
            if tcpCliSock is None:
                print("tcpCliSock is None")
                tcpCliSock = socket(AF_INET,SOCK_STREAM)
                tcpCliSock.connect(ADDR)

            data=tcpCliSock.recv(BUFSIZ)
            # print("loop recv:",data)
            if "RESP_NOTIFY" in data.decode('utf8'):
                print("recv notify!")
                if cache.get('notify') is not None:
                    tmp = cache.get('notify')
                    tmp.append(data.decode('utf8'))
                    # print("tmp is ",tmp)
                    cache.set('notify',tmp,10)
                else:
                    # print("notify is none")
                    tmp = []
                    tmp.append(data.decode('utf8'))
                    cache.set('notify',tmp,10)
                continue
            g = re.search('SeqNumber:\d+',data.decode('utf8'))
            if g is not None:
                # print(g.group())
                with lock:
                    # global recvDict
                    cache.set(g.group(),data.decode('utf8'),10)
                    # recvDict[g.group()] = data.decode('utf8')
                    # cache.set('recvDict',recvDict,10)
                    # print(cache.get('recvDict').keys())
        except BaseException as e:
            print("loop error:",e)
            tcpCliSock = None
    print("out loop!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
t = threading.Thread(target=loop)
t.start()



def brokenpipeHandle():
    pass

def makeConnection():
    global tcpCliSock

    global recvDict

    with lock:
        global seqNumber
        seqNumber+=1
    if tcpCliSock is not None:
        tcpCliSock.close()
    tcpCliSock = None
    while tcpCliSock is None:
        try:
            tcpCliSock = socket(AF_INET,SOCK_STREAM)
            tcpCliSock.connect(ADDR)

        except BaseException as e:
            tcpCliSock = None
            print(e)
            time.sleep(3)
    return True

def checkReturnIsNotifyOrNot(ret):
    isnotify = ("RESP_NOTIFYOFFLINE" in ret)
    return isnotify




# ------------------------------------------------------------------------------------------------------------------------------------------

def setmeetgeneraparaTask(meetName="",meetMode="0",meetType="0"):
    print("running task")
    global tcpCliSock



    with lock:
        global seqNumber
        seqNumber+=1


    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("setmeetgenerapara task")
    try:
        tcpCliSock.send(("SETMEETGENERALPARA\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMeetMode:%s\r\nMeetType:%s\r\n\r\n" % (seqNumber,meetName,meetMode,meetType)).encode('utf8'))
        time.sleep(0.2)
        key = "SeqNumber:"+str(seqNumber)
        for i in range(0,5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        return data
    # 开始连接成功，后来MCU断开连接了
    except ConnectionResetError as e:
        print("ConnectionResetError error: ",e)

    # 没连接到MCU
    except BrokenPipeError as e:
        print("BrokenPipeError: ",e)

    except IOError as e:
        print("ioerror:",e)
        return None
    except BaseException as e:
        print("BaseException: ",e)


def addmeetTask(meetName="",meetAlias="",meetRemark=""):
    global tcpCliSock



    with lock:
        global seqNumber
        seqNumber+=1
    if meetName is "":
        return "param error"
    if tcpCliSock is None:

        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("addmeetTask task")
    try:
        tcpCliSock.send(("ADDMEET\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMeetAlias:%s\r\nMeetRemark:%s\r\n\r\n" % (seqNumber,meetName,meetAlias,meetRemark)).encode('utf8'))
        time.sleep(0.2)
        key = "SeqNumber:"+str(seqNumber)
        for i in range(0,5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        return data
    # 开始连接成功，后来MCU断开连接了
    except ConnectionResetError as e:
        print("ConnectionResetError error: ",e)


    # 没连接到MCU
    except BrokenPipeError as e:
        print("BrokenPipeError: ",e)

    except IOError as e:
        print("ioerror:",e)
        return None
    except BaseException as e:
        print("BaseException: ",e)


def deletemeetTask(meetName=""):
    global tcpCliSock



    with lock:
        global seqNumber
        seqNumber+=1


    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("deletemeetTask task")
    try:
        tcpCliSock.send(("DELETEMEET\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\n\r\n" % (seqNumber,meetName)).encode('utf8'))
        time.sleep(0.2)
        key = "SeqNumber:"+str(seqNumber)
        for i in range(0,5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        return None
    # 开始连接成功，后来MCU断开连接了
    except ConnectionResetError as e:
        print("ConnectionResetError error: ",e)
        #
    # 没连接到MCU
    except BrokenPipeError as e:
        print("BrokenPipeError: ",e)

    except IOError as e:
        print("ioerror:",e)
    except BaseException as e:
        print("BaseException: ",e)
        #


def listmeetTask():
    global tcpCliSock



    with lock:
        global seqNumber
        seqNumber+=1

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("listmeetTask task")
    try:
        tcpCliSock.send(("LISTMEET\r\nVersion:1\r\nSeqNumber:%d\r\n\r\n" % seqNumber).encode('utf8'))
        time.sleep(0.2)
        key = "SeqNumber:"+str(seqNumber)
        for i in range(0,5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("BaseException: ",e)
        tcpCliSock = None

def addmemberTask(meetName="",memberName="0",memberIP="0"):
    global tcpCliSock



    with lock:
        global seqNumber
        seqNumber+=1
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("addmemberTask task")
    try:
        msg = ("ADDMEMBER\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\nMemberIP:%s\r\nMemberE164Alias:%s\r\nMemberH232Alias:%s\r\n\r\n" \
            % (seqNumber,meetName,memberName,memberIP,memberName,memberName))
        # print(msg)
        tcpCliSock.send(msg.encode('utf8'))
        time.sleep(0.2)
        key = "SeqNumber:"+str(seqNumber)
        for i in range(0,5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("BaseException: ",e)
        tcpCliSock = None
        return None

def setmemberavformatparaTask(meetName="",memberName="0",capalityName="1080P"):
    global tcpCliSock



    with lock:
        global seqNumber
        seqNumber+=1
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("addmemberTask task")
    try:
        msg = ("SETMEMBERAVFORMATPARA\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\nCapabilityName:%s\r\n\r\n" \
            % (seqNumber,meetName,memberName,capalityName))
        # print(msg)
        tcpCliSock.send(msg.encode('utf8'))
        time.sleep(0.2)
        key = "SeqNumber:"+str(seqNumber)
        for i in range(0,5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("BaseException: ",e)
        tcpCliSock = None
        return None

def callmemberTask(meetName="",memberName="0"):
    global tcpCliSock



    with lock:
        global seqNumber
        seqNumber+=1
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("callmemberTask task")
    try:
        msg = ("CALLMEMBER\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\n\r\n" \
            % (seqNumber,meetName,memberName))
        # print(msg)
        tcpCliSock.send(msg.encode('utf8'))
        time.sleep(0.2)
        key = "SeqNumber:"+str(seqNumber)
        for i in range(0,5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("callmemberTask BaseException: ",e)
        tcpCliSock = None
        return None

def checkNet():
    print("checkNet!")
    global tcpCliSock



    with lock:
        global seqNumber
        seqNumber+=1
    if tcpCliSock is not None:
        try:
            tcpCliSock.send(("HEARTBEAT\r\nVersion:1\r\nSeqNumber:%d\r\n\r\n" % seqNumber).encode('utf8'))
            time.sleep(0.2)
            key = "SeqNumber:"+str(seqNumber)
            for i in range(0,5):
                data = cache.get(key)
                if data is None:
                    time.sleep(0.1)
                    continue
                else:
                    # print("checknet ",data)
                    return data
            return None
        except BaseException as e:
            print("schedule error: ",e)
            tcpCliSock.close()
            tcpCliSock = socket(AF_INET,SOCK_STREAM)
            tcpCliSock.connect(ADDR)
            return "error"
    else:
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)

        return "error"

def addavformatpara(meetname='',capalityname='',callbandwidth='',audioprotocol='',videoprotocol='',videoformat='',videoframerate=60):
    global tcpCliSock



    with lock:
        global seqNumber
        seqNumber+=1
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("addavformatpara task")
    try:
        msg = ("ADDAVFORMATPARA\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nCapabilityName:%s\r\nCallBandWidth:%s\r\nAudioProtocol:%s\r\nVideoProtocol:%s\r\nVideoFormat:%s\r\nVideoFrameRate:%d\r\n\r\n" \
            % (seqNumber,meetname,capalityname,callbandwidth,audioprotocol,videoprotocol,videoformat,videoframerate)).encode('utf8')
        tcpCliSock.send(msg)
        time.sleep(0.2)
        key = "SeqNumber:"+str(seqNumber)
        for i in range(0,5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("BaseException: ",e)
        tcpCliSock = None
        return None

def setdualformatparaTask(meetname="",dualprotocol='',dualformat='',dualBandWidth=1024):
    global tcpCliSock



    with lock:
        global seqNumber
        seqNumber+=1
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("setdualformatparaTask task")
    try:
        msg = ("SETDUALFORMATPARA\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nDualProtocol:%s\r\nDualFormat:%s\r\nDualBandWidth:%d\r\n\r\n" \
            % (seqNumber,meetname,dualprotocol,dualformat,dualBandWidth)).encode('utf8')
        tcpCliSock.send(msg)
        time.sleep(0.2)
        key = "SeqNumber:"+str(seqNumber)
        for i in range(0,5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("setdualformatparaTask BaseException: ",e)
        tcpCliSock = None
        return None

def getmeetinfoTask(meetName=""):
    global tcpCliSock



    with lock:
        global seqNumber
        seqNumber+=1
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("getmeetinfoTask task")
    try:
        msg = ("GETMEETINFO\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\n\r\n" \
            % (seqNumber,meetName))
        tcpCliSock.send(msg.encode('utf8'))
        time.sleep(0.2)
        key = "SeqNumber:"+str(seqNumber)

        for i in range(0,5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("getmeetinfoTask BaseException: ",e)
        tcpCliSock = None
        return None


def hungupmemberTask(meetname,membername):
    global tcpCliSock
    with lock:
        global seqNumber
        seqNumber+=1
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("hungupmemberTask task")
    try:
        msg = ("HUNGUPMEMBER\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\n\r\n" \
            % (seqNumber,meetname,membername)).encode('utf8')
        tcpCliSock.send(msg)
        time.sleep(0.2)
        key = "SeqNumber:"+str(seqNumber)
        for i in range(0,5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        print("hungupmemberTask return None")
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("hungupmemberTask BaseException: ",e)
        tcpCliSock = None
        return None

def mutememberTask(meetname,membername,isMuting=0):
    global tcpCliSock
    with lock:
        global seqNumber
        seqNumber+=1
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("mutememberTask task")
    try:
        msg = ("SETMEMBERAUDIOMUTING\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\nMutingMode:%d\r\n\r\n" \
            % (seqNumber,meetname,membername,isMuting)).encode('utf8')
        print(msg)
        tcpCliSock.send(msg)
        time.sleep(0.2)
        key = "SeqNumber:"+str(seqNumber)
        for i in range(0,5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        print("mutememberTask return None")
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("hungupmemberTask BaseException: ",e)
        tcpCliSock = None
        return None

def audioblockTask(meetname,membername,isBlock=0):
    global tcpCliSock
    with lock:
        global seqNumber
        seqNumber+=1
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("audioblockTask task")
    try:
        msg = ("SETMEMBERAUDIOBLOCKING\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\nBlockingMode:%d\r\n\r\n" \
            % (seqNumber,meetname,membername,isBlock)).encode('utf8')
        print(msg)
        tcpCliSock.send(msg)
        time.sleep(0.2)
        key = "SeqNumber:"+str(seqNumber)
        for i in range(0,5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        print("audioblockTask return None")
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("audioblockTask BaseException: ",e)
        tcpCliSock = None
        return None

def getmemberinfoTask(meetname,membername):
    global tcpCliSock
    with lock:
        global seqNumber
        seqNumber+=1
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("getmemberinfoTask task")
    try:
        msg = ("GETMEMBERINFO\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\n\r\n" \
            % (seqNumber,meetname,membername)).encode('utf8')
        tcpCliSock.send(msg)
        time.sleep(0.05)
        key = "SeqNumber:"+str(seqNumber)
        for i in range(0,5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        print("getmemberinfoTask return None")
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("getmemberinfoTask BaseException: ",e)
        tcpCliSock = None
        return None

def deletememberTask(meetname,membername):
    global tcpCliSock
    with lock:
        global seqNumber
        seqNumber+=1
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("deletememberTask task")
    try:
        msg = ("DELETEMEMBER\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\n\r\n" \
            % (seqNumber,meetname,membername)).encode('utf8')
        print(msg)
        tcpCliSock.send(msg)
        time.sleep(0.2)
        key = "SeqNumber:"+str(seqNumber)
        for i in range(0,5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        print("deletememberTask return None")
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("deletememberTask BaseException: ",e)
        tcpCliSock = None
        return None








# ------------------------------------------------------------------------

def syncMeetingListAndDB(result):
    meeting.objects.all().update(activeInMcu=False)
    meetingNumber = result['MeetCount']
    # print(result)
    for index in range(0,int(meetingNumber)):
        filtered = meeting.objects.filter(name=result['MeetName'][index],meetcode=result['MeetAlias'][index])
        if  filtered.exists():
            print("esists!")
            filtered.update(activeInMcu=True)
        else:
            meeting(name=result['MeetName'][index],meetcode=result['MeetAlias'][index],remark = result['MeetRemark'][index]).save()
        # else:
        #     filtered.update(remark = result['MeetRemark'][index])

def analysisMeetinfo(retCode):
	if type(retCode) is not str:
		return False
	s = re.sub(r'\r\n\r\n','',retCode)
	a = s.split('\r\n')
	retDict = {}
	for item in a:
	    res = re.split(r':',item,1)
	    # print(res)
	    if len(res)<2:
	        retDict['RetName'] = res[0]
	    else:
	        retDict[res[0]] = res[1]
	meetInfo = re.split('\|',retDict['MemberList'])
	for item in meetInfo:
		# print(item)
		deep1 = re.split(r';',item)
		# print("deep1: ",deep1)
		for itemD1 in deep1:
			deep2 = re.split(r'\=',itemD1,1)
			# print(deep2)
			if deep2[0] in retDict and len(deep2) > 1:
				retDict[deep2[0]].append(deep2[1])
			elif len(deep2) > 1:
				retDict[deep2[0]] = []
				retDict[deep2[0]].append(deep2[1])
	return retDict

# ---------------------------------------------------------------------------------------------------------------------

@login_required
def creat_meetingView(request):
    if request.POST:
        meetform = meetingForm(request.POST)
        if meetform.is_valid():
            meetName = meetform.cleaned_data['name']
            MeetAlias = meetform.cleaned_data['meetcode']
            meetRemark = meetform.cleaned_data['remark']

            meetInstance = meetform.save()

            bandwidth = meetInstance.bandwidth
            videoprotocol = meetInstance.videoProtocol
            videoframerate = meetInstance.videoFrameRate
            capalityname = meetInstance.capalityname
            audioprotocol = meetInstance.audioProtocol

            dualProtocol = meetInstance.dualProtocol
            dualFormat = meetInstance.dualFormat
            dualBandWidth = meetInstance.dualBandWidth
            try:
                data = addmeetTask(meetName,MeetAlias,meetRemark)
                # print("addmeetTask result:",data)
            except BaseException as e:
                print("timeout error: ",e)
                msgType = 'error'
                msg = "操作：添加会议，连接MCU超时"
                meetinglist = meeting.objects.all()
                return render(request,'fun/meetinglist.html',{'meetinglist':meetinglist,'msgType':msgType,'msg':msg})


            try:
                data = setmeetgeneraparaTask(meetName)
                # print("setmeetgeneraparaTask result:",data)
            except BaseException as e:
                print("setmeetgeneraparaTask timeout error: ",e)
                msgType = 'error'
                msg = "操作：设置会议参数，连接MCU超时"
                meetinglist = meeting.objects.all()
                return render(request,'fun/meetinglist.html',{'meetinglist':meetinglist,'msgType':msgType,'msg':msg})


            result = addavformatpara(meetName,capalityname,bandwidth,audioprotocol,videoprotocol,capalityname,videoframerate)
            try:
                data = result
                retDict = returnCode2Dict(data)
                if retDict['RetCode'] == "200":
                    print("addavformatparaTask return 200ok")
            except BaseException as e:
                print("addavformatparaTask timeout error: ",e)
                msgType = 'error'
                msg = "操作：设置会议格式参数，连接MCU超时"
                meetinglist = meeting.objects.all()
                return render(request,'fun/meetinglist.html',{'meetinglist':meetinglist,'msgType':msgType,'msg':msg})

            result = setdualformatparaTask(meetName,dualProtocol,dualFormat,dualBandWidth)
            try:
                data = result
                retDict = returnCode2Dict(data)
                if retDict['RetCode'] == "200":
                    print("setdualformatparaTask return 200ok")
                    return redirect(meetinglistView)
            except BaseException as e:
                print("setdualformatparaTask timeout error: ",e)
                msgType = 'error'
                msg = "操作：设置会议双流参数，连接MCU超时"
                meetinglist = meeting.objects.all()
                return render(request,'fun/meetinglist.html',{'meetinglist':meetinglist,'msgType':msgType,'msg':msg})
            return redirect(meetinglistView)
        else:
            return render(request,'fun/creat_meeting.html',{'meetform':meetform,'msgType':"error",'msg':"填写错误，请重新提交"})
    else:
        meetform = meetingForm()
        return render(request,'fun/creat_meeting.html',{'meetform':meetform,'msgType':"info",'msg':"请添加会议"})

@login_required
def delete_meetingView(request,meetpk):
    if not meeting.objects.filter(pk=meetpk).exists():
        print("该会议不存在！")
        msgType = "error"
        msg = "该会议不存在"
        meetinglist = meeting.objects.all()
        return render(request,'fun/meetinglist.html',{'meetinglist':meetinglist,'msgType':msgType,'msg':msg})
    else:
        meeting.objects.get(pk=meetpk).delete()
        msgType = "success"
        msg = "删除成功"
        meetinglist = meeting.objects.all()
        return render(request,'fun/meetinglist.html',{'meetinglist':meetinglist,'msgType':msgType,'msg':msg})


@login_required
def meetinglistView(request,msgType='',msg=''):
    try:
        data = listmeetTask()

    except BaseException as e:
        print("timeout error: ",e)
        msgType = "error"
        msg = "连接MCU失败，显示数据库备份内容"
        meetinglist = meeting.objects.all()
        return render(request,'fun/meetinglist.html',{'meetinglist':meetinglist,'msgType':msgType,'msg':msg})
    if not data:
        msgType = "error"
        msg = "连接MCU失败，显示数据库备份内容"
        meetinglist = meeting.objects.all()
        return render(request,'fun/meetinglist.html',{'meetinglist':meetinglist,'msgType':msgType,'msg':msg})
    result = analysisListMeetResult(data)
    syncMeetingListAndDB(result)
    msgType = "nothing"
    msg = "未知连接错误，将显示数据库备份内容"
    meetinglist = meeting.objects.all()
    return render(request,'fun/meetinglist.html',{'meetinglist':meetinglist,'msgType':msgType,'msg':msg})


# @login_required
# def meetinglistView(request):
#     return render(request,'meeting_manage/meetinglist.html')

@login_required
def terminallistView(request,msgType='',msg=''):
    terminalList = terminal.objects.all()
    return render(request,'fun/terminallist.html',{'terminallist':terminalList,'msgType':msgType,'msg':msg})



@login_required
def addterminalView(request):
    if request.POST:
        terminalform = terminalForm(request.POST)
        if terminalform.is_valid():
            terminalform.save(commit=True)
            terminalList = terminal.objects.all()
            # return HttpResponseRedirect('/terminallist',msg="1234")
            # return HttpResponseRedirect(reverse('terminallist', kwargs={'msg': 'auth'}))
            return terminallistView(request,"success","add success!")
            return render(request,'fun/terminallist.html',{'terminallist':terminalList,'msgType':'success','msg':"add success!!!!"})
        else:
            return render(request,'fun/addterminal.html',{'terminalform':terminalform,'msgType':'error','msg':"fail to add"})
    else:
        terminalform = terminalForm()
        return render(request,'fun/addterminal.html',{'terminalform':terminalform,'msgType':'info','msg':"please add"})

@login_required
def terminallistViewP(request,msg):
    terminalList = terminal.objects.all()
    return render(request,'fun/terminallist.html',{'terminallist':terminalList,'msgType':'info','msg':msg})

@login_required
def templatelistView(request,msgType='',msg=''):
    templateList = meetingTemplate.objects.all()
    return render(request,'fun/templatelist.html',{'templatelist':templateList,'msgType':msgType,'msg':msg})

@login_required
def addtemplateView(request):
    if request.POST:
        templateform = meetingTemplateForm(request.POST)
        if templateform.is_valid():
            templateform.save(commit=True)
            templateList = meetingTemplate.objects.all()
            return render(request,'fun/templatelist.html',{'templatelist':templateList,'msgType':'success','msg':'add success'})
        else:
            return render(request,'fun/addtemplate.html',{'templateform':templateform,'msgType':'error','msg':"fail to add"})
    else:
        templateform = meetingTemplateForm()
        return render(request,'fun/addtemplate.html',{'templateform':templateform,'msgType':'info','msg':"please add"})

# Ajax Views
# ---------------------------------------------------------------------------

@login_required
def heartBeatAjaxView(request):
    if request.is_ajax():
        print("recv heartBeat ajax request")
        result=""
        try:
            result = checkNet()
            if result is None:
                return HttpResponse(False)
            # print("heart beat check result is: \n",result)
        except BaseException as e:
            print("catch heartbeat error",e)
            return HttpResponse(False)
        return HttpResponse(True)

@login_required
def callmemberAjaxView(request,meetpk,pk):
    if request.is_ajax():
        print("recv callmember ajax request")
        result=""
        if not meeting.objects.filter(pk=meetpk).exists():
            print("该会议不存在！")
            return HttpResponse(json.dumps({'msgType':"error",'msg':"该会议不存在！"}))
        if not terminal.objects.filter(pk=pk).exists():
            print("该终端不存在！")
            return HttpResponse(json.dumps({'msgType':"error",'msg':"该终端不存在！"}))
        meetname = meeting.objects.get(pk=meetpk).name
        membername = terminal.objects.get(pk=pk).name
        memberip = terminal.objects.get(pk=pk).terminalIP

        capability = terminal.objects.get(pk=pk).capalityname
        # add member
        try:
            result = addmemberTask(meetname,membername,memberip)
            # print("add member check result is: \n",result)
        except BaseException as e:
            print("catch add member error",e)
            return HttpResponse(json.dumps({'msgType':"error",'msg':"向会议中添加终端过程中发生通信错误！"}))
        if result is None:
            print("add member return None")
            return HttpResponse(json.dumps({'msgType':"error",'msg':"向会议中添加终端过程中MCU返回None！"}))
        retDict = returnCode2Dict(result)
        if retDict['RetCode'] != "200":
            # print("addmemberTask return %s" % retDict['RetCode'])
            return HttpResponse(json.dumps({'msgType':"error",'msg':("向会议中添加终端过程中MCU返回%s！" % retDict['RetCode'])}))
        # setmemberavformatpara
        try:
            result = setmemberavformatparaTask(meetname,membername,capability)
            # print("setmemberavformatpara check result is: \n",result)
        except BaseException as e:
            print("catch setmemberavformatpara error",e)
            return HttpResponse(json.dumps({'msgType':"error",'msg':"向会议中添加终端参数过程中发生通信错误！"}))
        if result is None:
            print("setmemberavformatpara return None")
            return HttpResponse(json.dumps({'msgType':"error",'msg':"向会议中添加终端参数过程中MCU返回None！"}))
        retDict = returnCode2Dict(result)
        if retDict['RetCode'] != "200":
            print("setmemberavformatpara return %s" % retDict['RetCode'])
            return HttpResponse(json.dumps({'msgType':"error",'msg':("向会议中添加终端参数过程中MCU返回%s！" % retDict['RetCode'])}))
        # callmember
        try:
            result = callmemberTask(meetname,membername)
            # print("callmemberTask result is: \n",result)
        except BaseException as e:
            print("catch callmemberTask error",e)
            return HttpResponse(json.dumps({'msgType':"error",'msg':"呼叫终端过程中发生通信错误！"}))
        if result is None:
            print("callmemberTask return None")
            return HttpResponse(json.dumps({'msgType':"error",'msg':"呼叫终端过程中MCU返回None！"}))
        retDict = returnCode2Dict(result)
        if retDict['RetCode'] != "200":
            # print("callmemberTask return %s" % retDict['RetCode'])
            return HttpResponse(json.dumps({'msgType':"error",'msg':("呼叫终端过程中MCU返回%s！" % retDict['RetCode'])}))
        # time.sleep(0.5)

        # getmemberinfoTask
        result = getmemberinfoTask(meetname,membername)
        # print("getmemberinfoTask return: ",result)
        retcode = returnCode2Dict(result)
        retcode["pk"] = pk
        return HttpResponse(json.dumps(retcode))
        # print(analysis(result))

        return HttpResponse(json.dumps({'msgType':"success",'msg':"操作成功！"}))

@login_required
def getmeetinfoAjaxView(request,meetpk):
    if request.is_ajax():
        print("recv getmeetinfo ajax request")
        result=""
        if not meeting.objects.filter(pk=meetpk).exists():
            print("该会议不存在！")
            return HttpResponse(json.dumps({'msgType':"error",'msg':"该会议不存在！"}))

        meetname = meeting.objects.get(pk=meetpk).name
        # getmeetinfo
        try:

            result = getmeetinfoTask(meetname)
            notifyList = cache.get('notify')
            if notifyList is not None:
                print(notifyList)
                cache.delete('notify')
            # print("getmeetinfo result is: \n",result)
            if result is not None:
                analysysResult = analysisMeetinfo(result)
                # analysysResult['']
                if "EPName" in analysysResult.keys():
                    analysysResult['pk'] = []
                    for ename in analysysResult['EPName']:
                        if terminal.objects.filter(name = ename).exists():
                            analysysResult['pk'].append(terminal.objects.get(name = ename).pk)
                        else:
                            analysysResult['pk'].append("None")
                # print(analysysResult)
                return HttpResponse(json.dumps(analysysResult))
        except BaseException as e:
            print("catch getmeetinfo error",e,"-----",result)
            return HttpResponse(json.dumps({'msgType':"error",'msg':"获取会议信息过程中发生通信错误！"}))
        if result is None:
            print("getmeetinfo return None")
            return HttpResponse(json.dumps({'msgType':"error",'msg':"获取会议信息过程中MCU返回None！"}))
        retDict = returnCode2Dict(result)
        if retDict['RetCode'] != "200":
            # print("getmeetinfo return %s" % retDict['RetCode'])
            return HttpResponse(json.dumps({'msgType':"error",'msg':("获取会议信息过程中MCU返回%s！" % retDict['RetCode'])}))
        return HttpResponse(json.dumps({'msgType':"success",'msg':"操作成功！"}))

@login_required
def hungupAjaxView(request,meetpk,pk):
    if request.is_ajax():
        print("recv hungupAjaxView ajax request")
        result=""
        if not meeting.objects.filter(pk=meetpk).exists():
            print("该会议不存在！")
            return HttpResponse(json.dumps({'msgType':"error",'msg':"该会议不存在！"}))
        if not terminal.objects.filter(pk=pk).exists():
            print("该终端不存在！")
            return HttpResponse(json.dumps({'msgType':"error",'msg':"该终端不存在！"}))
        meetname = meeting.objects.get(pk=meetpk).name
        membername = terminal.objects.get(pk=pk).name
        memberip = terminal.objects.get(pk=pk).terminalIP
        # hungupAjaxView
        try:

            result = hungupmemberTask(meetname,membername)
            notifyList = cache.get('notify')
            if notifyList is not None:
                # # print(notifyList)
                cache.delete('notify')
            if result is None:
                return HttpResponse(json.dumps({'msgType':"error",'msg':"挂断过程中MCU返回None！"}))
            result = deletememberTask(meetname,membername)
            notifyList = cache.get('notify')
            if notifyList is not None:
                # # print(notifyList)
                cache.delete('notify')
            if result is None:
                return HttpResponse(json.dumps({'msgType':"error",'msg':"挂断过程中MCU返回None！"}))
            return HttpResponse(json.dumps({'msgType':"success",'msg':"操作成功！"}))
        except BaseException as e:
            print("catch hungup error",e)
            return HttpResponse(json.dumps({'msgType':"error",'msg':"挂断过程中发生通信错误！"}))
        if result is None:
            print("hungup return None")
            return HttpResponse(json.dumps({'msgType':"error",'msg':"挂断过程中MCU返回None！"}))
        retDict = returnCode2Dict(result)
        if retDict['RetCode'] != "200":
            # print("getmeetinfo return %s" % retDict['RetCode'])
            return HttpResponse(json.dumps({'msgType':"error",'msg':("挂断过程中MCU返回%s！" % retDict['RetCode'])}))
        return HttpResponse(json.dumps({'msgType':"success",'msg':"操作成功！"}))

@login_required
def silencememberAjaxView(request,meetpk,pk):
    if request.is_ajax():
        print("recv silencememberAjaxView ajax request")
        result=""
        if not meeting.objects.filter(pk=meetpk).exists():
            print("该会议不存在！")
            return HttpResponse(json.dumps({'msgType':"error",'msg':"该会议不存在！"}))
        if not terminal.objects.filter(pk=pk).exists():
            print("该终端不存在！")
            return HttpResponse(json.dumps({'msgType':"error",'msg':"该终端不存在！"}))
        meetname = meeting.objects.get(pk=meetpk).name
        membername = terminal.objects.get(pk=pk).name
        memberip = terminal.objects.get(pk=pk).terminalIP
        # hungupAjaxView
        try:

            result = mutememberTask(meetname,membername,1)
            notifyList = cache.get('notify')
            if notifyList is not None:
                # # print(notifyList)
                cache.delete('notify')
            if result is None:
                return HttpResponse(json.dumps({'msgType':"error",'msg':"挂断过程中MCU返回None！"}))
            print("mutememberTask return: ",result)
            result = getmemberinfoTask(meetname,membername)

            notifyList = cache.get('notify')
            if notifyList is not None:
                pass
                # print(notifyList)
                # cache.delete('notify')
            if result is None:
                return HttpResponse(json.dumps({'msgType':"error",'msg':"挂断过程中MCU返回None！"}))
            print("getmemberinfoTask return: ",result)
            retcode = returnCode2Dict(result)
            retcode["pk"] = pk
            return HttpResponse(json.dumps(retcode))
        except BaseException as e:
            print("catch getmeetinfo error",e)
            return HttpResponse(json.dumps({'msgType':"error",'msg':"获取会议信息过程中发生通信错误！"}))
        if result is None:
            print("getmeetinfo return None")
            return HttpResponse(json.dumps({'msgType':"error",'msg':"获取会议信息过程中MCU返回None！"}))
        retDict = returnCode2Dict(result)
        if retDict['RetCode'] != "200":
            # print("getmeetinfo return %s" % retDict['RetCode'])
            return HttpResponse(json.dumps({'msgType':"error",'msg':("获取会议信息过程中MCU返回%s！" % retDict['RetCode'])}))
        return HttpResponse(json.dumps({'msgType':"success",'msg':"操作成功！"}))

@login_required
def audioblockAjaxView(request,meetpk,pk):
    if request.is_ajax():
        print("recv audioblockAjaxView ajax request")
        result=""
        if not meeting.objects.filter(pk=meetpk).exists():
            print("该会议不存在！")
            return HttpResponse(json.dumps({'msgType':"error",'msg':"该会议不存在！"}))
        if not terminal.objects.filter(pk=pk).exists():
            print("该终端不存在！")
            return HttpResponse(json.dumps({'msgType':"error",'msg':"该终端不存在！"}))
        meetname = meeting.objects.get(pk=meetpk).name
        membername = terminal.objects.get(pk=pk).name
        memberip = terminal.objects.get(pk=pk).terminalIP
        # hungupAjaxView
        try:

            result = audioblockTask(meetname,membername,1)
            notifyList = cache.get('notify')
            if notifyList is not None:
                # # print(notifyList)
                cache.delete('notify')
            if result is None:
                return HttpResponse(json.dumps({'msgType':"error",'msg':"禁言过程中MCU返回None！"}))
            print("mutememberTask return: ",result)
            result = getmemberinfoTask(meetname,membername)

            notifyList = cache.get('notify')
            if notifyList is not None:
                pass
                # print(notifyList)
                # cache.delete('notify')
            if result is None:
                return HttpResponse(json.dumps({'msgType':"error",'msg':"禁言过程中MCU返回None！"}))
            print("getmemberinfoTask return: ",result)
            retcode = returnCode2Dict(result)
            retcode["pk"] = pk
            return HttpResponse(json.dumps(retcode))
        except BaseException as e:
            print("catch getmeetinfo error",e)
            return HttpResponse(json.dumps({'msgType':"error",'msg':"禁言过程中发生通信错误！"}))
        if result is None:
            print("getmeetinfo return None")
            return HttpResponse(json.dumps({'msgType':"error",'msg':"禁言过程中MCU返回None！"}))
        retDict = returnCode2Dict(result)
        if retDict['RetCode'] != "200":
            # print("getmeetinfo return %s" % retDict['RetCode'])
            return HttpResponse(json.dumps({'msgType':"error",'msg':("禁言过程中MCU返回%s！" % retDict['RetCode'])}))
        return HttpResponse(json.dumps({'msgType':"success",'msg':"操作成功！"}))


# ---------------------------------------------------------------------------

@login_required
def meetDetailsView(request,meetpk):
    meetInstance = meeting.objects.get(pk=meetpk)
    terminalList = terminal.objects.all()
    return render(request,'fun/meetDetail.html',{'meetInstance':meetInstance,'terminalList':terminalList,'msgType':'info','msg':"please add"})
