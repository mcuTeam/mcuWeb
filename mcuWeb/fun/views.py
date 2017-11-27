from __future__ import absolute_import, unicode_literals
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse,HttpResponseServerError
import threading
import json

from fun.forms import *
from system.models import *
from system.views import *
import re

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

try:
    tcpCliSock = socket(AF_INET,SOCK_STREAM)
    tcpCliSock.connect(ADDR)

except BaseException as e:
    tcpCliSock = None
    print(e)
    print("1")

def loop():
    global tcpCliSock
    global recvDict
    while True:
        data=tcpCliSock.recv(BUFSIZ)
        # print("loop recv:",data)
        g = re.search('SeqNumber:\d+',data.decode('utf8'))
        if g is not None:
            # print(g.group())
            recvDict[g.group()] = data.decode('utf8')
t = threading.Thread(target=loop)
t.start()



def brokenpipeHandle():
    pass

def makeConnection():
    global tcpCliSock
    global seqNumber
    global recvDict
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
    print(isnotify)
    return isnotify

# ------------------------------------------------------------------------------------------------------------------------------------------

def setmeetgeneraparaTask(meetName="",meetMode="0",meetType="0"):
    print("running task")
    global tcpCliSock
    global seqNumber
    global recvDict
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
        if key not in recvDict.keys():
            print("in keys ")
            return None
        data = recvDict[key]
        print(seqNumber,'-------',data)
        del recvDict[key]
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
    global seqNumber
    global recvDict
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
        if key not in recvDict.keys():
            print("in keys ")
            return None
        data = recvDict[key]
        print(seqNumber,'-------',data)
        del recvDict[key]
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
    global seqNumber
    global recvDict
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
        if key not in recvDict.keys():
            print("in keys ")
            return None
        data = recvDict[key]
        print(seqNumber,'-------',data)
        del recvDict[key]
        return data
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
    global seqNumber
    global recvDict
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
        if key not in recvDict.keys():
            print("in keys ")
            return None
        data = recvDict[key]
        print(seqNumber,'-------',data)
        del recvDict[key]
        return data
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("BaseException: ",e)
        tcpCliSock = None

def addmemberTask(meetName="",memberName="0",memberIP="0"):
    global tcpCliSock
    global seqNumber
    global recvDict
    seqNumber+=1
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("addmemberTask task")
    try:
        msg = ("ADDMEMBER\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\nMemberIP:%s\r\nMemberE164Alias:%s\r\nMemberH232Alias:%s\r\n\r\n" \
            % (seqNumber,meetName,memberName,memberIP,memberName,memberName))
        print(msg)
        tcpCliSock.send(msg.encode('utf8'))
        time.sleep(0.2)
        key = "SeqNumber:"+str(seqNumber)
        if key not in recvDict.keys():
            print("in keys ")
            return None
        data = recvDict[key]
        print(seqNumber,'-------',data)
        del recvDict[key]
        return data
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("BaseException: ",e)
        tcpCliSock = None
        return None

def setmemberavformatparaTask(meetName="",memberName="0",capalityName="1080P"):
    global tcpCliSock
    global seqNumber
    global recvDict
    seqNumber+=1
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("addmemberTask task")
    try:
        msg = ("SETMEMBERAVFORMATPARA\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\nCapabilityName:%s\r\n\r\n" \
            % (seqNumber,meetName,memberName,capalityName))
        print(msg)
        tcpCliSock.send(msg.encode('utf8'))
        time.sleep(0.2)
        key = "SeqNumber:"+str(seqNumber)
        if key not in recvDict.keys():
            print("in keys ")
            return None
        data = recvDict[key]
        print(seqNumber,'-------',data)
        del recvDict[key]
        return data
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("BaseException: ",e)
        tcpCliSock = None
        return None

def callmemberTask(meetName="",memberName="0"):
    global tcpCliSock
    global seqNumber
    global recvDict
    seqNumber+=1
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET,SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("callmemberTask task")
    try:
        msg = ("CALLMEMBER\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\n\r\n" \
            % (seqNumber,meetName,memberName))
        print(msg)
        tcpCliSock.send(msg.encode('utf8'))
        time.sleep(0.2)
        key = "SeqNumber:"+str(seqNumber)
        if key not in recvDict.keys():
            print("in keys ")
            return None
        data = recvDict[key]
        print(seqNumber,'-------',data)
        del recvDict[key]
        return data
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("callmemberTask BaseException: ",e)
        tcpCliSock = None
        return None

def checkNet():
    print("checkNet!")
    global tcpCliSock
    global seqNumber
    global recvDict
    seqNumber+=1
    if tcpCliSock is not None:
        try:
            tcpCliSock.send(("HEARTBEAT\r\nVersion:1\r\nSeqNumber:%d\r\n\r\n" % seqNumber).encode('utf8'))
            time.sleep(0.2)
            key = "SeqNumber:"+str(seqNumber)
            if key not in recvDict.keys():
                print("in keys ")
                return None
            data = recvDict[key]
            print(seqNumber,'-------',data)
            del recvDict[key]
            return data
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
        if key not in recvDict.keys():
            print("in keys ")
            return None
        data = recvDict[key]
        print(seqNumber,'-------',data)
        del recvDict[key]
        return data
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("BaseException: ",e)
        tcpCliSock = None
        return None

def setdualformatparaTask(meetname="",dualprotocol='',dualformat='',dualBandWidth=1024):
    global tcpCliSock
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
        if key not in recvDict.keys():
            print("in keys ")
            return None
        data = recvDict[key]
        print(seqNumber,'-------',data)
        del recvDict[key]
        return data
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("setdualformatparaTask BaseException: ",e)
        tcpCliSock = None
        return None

def getmeetinfoTask(meetName=""):
    global tcpCliSock
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
        print(msg)
        tcpCliSock.send(msg.encode('utf8'))
        time.sleep(0.2)
        key = "SeqNumber:"+str(seqNumber)
        if key not in recvDict.keys():
            print("in keys ")
            return None
        data = recvDict[key]
        print(seqNumber,'-------',data)
        del recvDict[key]
        return data
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("getmeetinfoTask BaseException: ",e)
        tcpCliSock = None
        return None













# ------------------------------------------------------------------------

def syncMeetingListAndDB(result):
	meeting.objects.all().update(activeInMcu=False)
	meetingNumber = result['MeetCount']
	for index in range(0,int(meetingNumber)):
		filtered = meeting.objects.filter(name=result['MeetName'][index],meetcode=result['MeetAlias'][index])
		if  filtered.exists():
			print("esists!")
			filtered.update(activeInMcu=True)
		# else:
		# 	filtered.update(remark = result['MeetRemark'][index])

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
				print("addmeetTask result:",data)
			except BaseException as e:
				print("timeout error: ",e)
				msgType = 'error'
				msg = "操作：添加会议，连接MCU超时"
				meetinglist = meeting.objects.all()
				return render(request,'fun/meetinglist.html',{'meetinglist':meetinglist,'msgType':msgType,'msg':msg})
			if data is None:
				print("return None")
				msgType = 'error'
				msg = "MCU未返回数据"
				meetinglist = meeting.objects.all()
				return render(request,'fun/meetinglist.html',{'meetinglist':meetinglist,'msgType':msgType,'msg':msg})

			ret = returnCode2Dict(data)
			if ret['RetCode'] != '200':
				print(ret['RetCode'] is '200')
				print("error0 occurs")
			result = setmeetgeneraparaTask(meetName)
			try:
				data = result
				print("setmeetgeneraparaTask result:",data)
			except BaseException as e:
				print("setmeetgeneraparaTask timeout error: ",e)
				msgType = 'error'
				msg = "操作：设置会议参数，连接MCU超时"
				meetinglist = meeting.objects.all()
				return render(request,'fun/meetinglist.html',{'meetinglist':meetinglist,'msgType':msgType,'msg':msg})
			ret.clear()
			if data is  None:
				print("return None")
				msgType = 'error'
				msg = "连接MCU超时"
				meetinglist = meeting.objects.all()
				return render(request,'fun/meetinglist.html',{'meetinglist':meetinglist,'msgType':msgType,'msg':msg})
			else:
				ret = returnCode2Dict(data)
				if ret['RetCode'] != '200':
					print(ret['RetCode'])
					print("error1 occurs")
				msgType = 'success'
				msg = "成功"
				# return redirect(meetinglistView)
				# return render(request,'fun/meetinglist.html',{'meetinglist':meetinglist,'msgType':msgType,'msg':msg})
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
		print("1")
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
# 	return render(request,'meeting_manage/meetinglist.html')

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
			print("heart beat check result is: \n",result)
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
			print("add member check result is: \n",result)
		except BaseException as e:
			print("catch add member error",e)
			return HttpResponse(json.dumps({'msgType':"error",'msg':"向会议中添加终端过程中发生通信错误！"}))
		if result is None:
			print("add member return None")
			return HttpResponse(json.dumps({'msgType':"error",'msg':"向会议中添加终端过程中MCU返回None！"}))
		retDict = returnCode2Dict(result)
		if retDict['RetCode'] != "200":
			print("addmemberTask return %s" % retDict['RetCode'])
			return HttpResponse(json.dumps({'msgType':"error",'msg':("向会议中添加终端过程中MCU返回%s！" % retDict['RetCode'])}))
		# setmemberavformatpara
		try:
			result = setmemberavformatparaTask(meetname,membername,capability)
			print("setmemberavformatpara check result is: \n",result)
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
			print("callmemberTask result is: \n",result)
		except BaseException as e:
			print("catch callmemberTask error",e)
			return HttpResponse(json.dumps({'msgType':"error",'msg':"呼叫终端过程中发生通信错误！"}))
		if result is None:
			print("callmemberTask return None")
			return HttpResponse(json.dumps({'msgType':"error",'msg':"呼叫终端过程中MCU返回None！"}))
		retDict = returnCode2Dict(result)
		if retDict['RetCode'] != "200":
			print("callmemberTask return %s" % retDict['RetCode'])
			return HttpResponse(json.dumps({'msgType':"error",'msg':("呼叫终端过程中MCU返回%s！" % retDict['RetCode'])}))
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
			print("getmeetinfo result is: \n",result)
		except BaseException as e:
			print("catch getmeetinfo error",e)
			return HttpResponse(json.dumps({'msgType':"error",'msg':"获取会议信息过程中发生通信错误！"}))
		if result is None:
			print("getmeetinfo return None")
			return HttpResponse(json.dumps({'msgType':"error",'msg':"获取会议信息过程中MCU返回None！"}))
		retDict = returnCode2Dict(result)
		if retDict['RetCode'] != "200":
			print("getmeetinfo return %s" % retDict['RetCode'])
			return HttpResponse(json.dumps({'msgType':"error",'msg':("获取会议信息过程中MCU返回%s！" % retDict['RetCode'])}))
		return HttpResponse(json.dumps({'msgType':"success",'msg':"操作成功！"}))

# ---------------------------------------------------------------------------

@login_required
def meetDetailsView(request,meetpk):
	meetInstance = meeting.objects.get(pk=meetpk)
	terminalList = terminal.objects.all()
	return render(request,'fun/meetDetail.html',{'meetInstance':meetInstance,'terminalList':terminalList,'msgType':'info','msg':"please add"})
