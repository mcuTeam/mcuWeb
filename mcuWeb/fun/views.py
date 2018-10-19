# coding:utf-8
from __future__ import print_function
from __future__ import print_function
from __future__ import absolute_import, unicode_literals

import ConfigParser
from configobj import ConfigObj
import os
import json
import re
import socket
import threading
import time
from socket import *
from threading import Lock

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import render, redirect

from fun.forms import *
from system.forms import *
from system.views import returnCode2Dict, analysisListMeetResult, homeView
from django.utils.translation import gettext as _

# Create your views here.


HOST = "127.0.0.1"
PORT = 5038
BUFSIZ = 10240
ADDR = (HOST, PORT)
tcpCliSock = None
# seqNumber = 0
cache.set('seqNumber', 0)
recvDict = {}
lock = Lock()

try:
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)

except BaseException as e:
    tcpCliSock = None


def loop():
    global tcpCliSock

    while True:
        try:
            if tcpCliSock is None:
                print("tcpCliSock is None")
                tcpCliSock = socket(AF_INET, SOCK_STREAM)
                tcpCliSock.connect(ADDR)

            data = tcpCliSock.recv(BUFSIZ)
            # print("loop recv:",data)
            if "RESP_NOTIFY" in data.decode('gb2312'):
                print("recv notify!",data.decode('gb2312'))
                if cache.get('notify') is not None:
                    tmp = cache.get('notify')
                    tmp.append(data.decode('gb2312'))
                    # print("tmp is ",tmp)
                    cache.set('notify', tmp, 10)
                else:
                    # print("notify is none")
                    tmp = []
                    tmp.append(data.decode('gb2312'))
                    cache.set('notify', tmp, 10)
                continue
            g = re.search('SeqNumber:\d+', data.decode('gb2312'))
            if g is not None:
                # print(g.group())

                # global recvDict
                cache.set(g.group(), data.decode('gb2312'), 10)
                # recvDict[g.group()] = data.decode('gb2312')
                # cache.set('recvDict',recvDict,10)
                # print(cache.get('recvDict').keys())
        except UnicodeDecodeError as e:
            print("loop decode error:",e)
        except BaseException as e:
            print("loop error:", e)
            tcpCliSock = None
            time.sleep(1.0)

    print("out loop!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")


t = threading.Thread(target=loop)
t.start()

exitFlag = 0


class call_all(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, meetName="", chairMan="", memberList=""):
        threading.Thread.__init__(self)
        self.meetName = meetName
        self.chairMan = chairMan
        self.memberList = memberList

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.meetName)
        HOST = "127.0.0.1"
        PORT = 5038
        BUFSIZ = 10240
        ADDR = (HOST, PORT)
        tcpCliSockInTask = None
        try:
            tcpCliSockInTask = socket(AF_INET, SOCK_STREAM)
            tcpCliSockInTask.connect(ADDR)
            tcpCliSockInTask.settimeout(3)
        except BaseException as e:
            tcpCliSockInTask = None
        memberList = json.loads(self.memberList)
        print("callallTask task", memberList, type(memberList))
        if tcpCliSockInTask is None:
            print("tcpCliSockInTask is None")
            tcpCliSockInTask = socket(AF_INET, SOCK_STREAM)
            tcpCliSockInTask.connect(ADDR)
            tcpCliSockInTask.settimeout(3)
        try:
            for member in memberList:
                # first addmember
                # second setmemberavformatparaTask

                memberName = member['name']
                memberIP = member['terminalIP']
                capalityName = member['capalityName']
                msg = (
                        "ADDMEMBER\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nMemberName:%s\r\nMemberIP:%s\r\nMemberE164Alias:%s\r\nMemberH232Alias:%s\r\n\r\n" \
                        % (self.meetName, memberName, memberIP, memberName, memberName))

                tcpCliSockInTask.send(msg.encode('gb2312'))
                time.sleep(0.05)
                msg = (
                        "SETMEMBERAVFORMATPARA\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\nMemberName:%s\r\nCapabilityName:%s\r\n\r\n" \
                        % (self.meetName, memberName, capalityName))

                tcpCliSockInTask.send(msg.encode('gb2312'))

                # if memberName == chairMan:
                #     print("-------------chairMan------------")
                #     time.sleep(0.05)
                #     msg = ("SETMEMBERIDENTITY\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\n\r\n" \
                #         % (1,meetName,memberName)).encode('gb2312')
                #     tcpCliSock.send(msg)
            # third callall
            # optional setidentity
            time.sleep(0.1)
            msg = "CALLALL\r\nVersion:1\r\nSeqNumber:1\r\nMeetName:%s\r\n\r\n" % (self.meetName)
            tcpCliSockInTask.send(msg.encode('gb2312'))
            print("wait", len(memberList))
            time.sleep(len(memberList) + 2)
            print("wait")
            msg = ("SETMEMBERIDENTITY\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\n\r\n"
                   % (1, self.meetName, self.chairMan)).encode('gb2312')
            tcpCliSockInTask.send(msg)

        except BaseException as e:
            print("BaseException: ", e)
            tcpCliSock = None
        print("Exiting " + self.name)


class hangup_all(threading.Thread):  # 继承父类threading.Thread
    def __init__(self, meetName="", memberList=""):
        threading.Thread.__init__(self)
        self.meetName = meetName
        self.memberList = memberList

    def run(self):  # 把要执行的代码写到run函数里面 线程在创建后会直接运行run函数
        print("Starting " + self.meetName)
        HOST = "127.0.0.1"
        PORT = 5038
        BUFSIZ = 10240
        ADDR = (HOST, PORT)
        tcpCliSockInTask = None
        try:
            tcpCliSockInTask = socket(AF_INET, SOCK_STREAM)
            tcpCliSockInTask.connect(ADDR)
            tcpCliSockInTask.settimeout(3)
        except BaseException as e:
            tcpCliSockInTask = None
        memberList = json.loads(self.memberList)
        print("callallTask task", memberList, type(memberList))
        try:
            msg = ("HUNGUPALL\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\n\r\n"
                   % (1, self.meetName)).encode('gb2312')
            tcpCliSockInTask.send(msg)
            time.sleep(0.5 * len(self.memberList))
            for member in self.memberList:
                # first addmember
                # second setmemberavformatparaTask

                msg = ("DELETEMEMBER\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\n\r\n"
                       % (1, self.meetName, member)).encode('gb2312')
                # print(msg)
                tcpCliSockInTask.send(msg)
                time.sleep(0.1)
            return None

        except BaseException as e:
            print("BaseException: ", e)
            tcpCliSockInTask = None


def returnCode2Dict(retCode):
    if type(retCode) is not unicode:
        return False
    s = re.sub(r'\r\n\r\n', '', retCode)
    a = s.split('\r\n')
    retDict = {}
    for item in a:
        res = re.split(r':', item, 1)
        if len(res) < 2:
            retDict['RetName'] = res[0]
        else:
            retDict[res[0]] = res[1]
    return retDict


def analysisListMeetResult(retCode):
    if type(retCode) is not unicode:
        return False
    s = re.sub(r'\r\n\r\n', '', retCode)
    a = s.split('\r\n')
    retDict = {}
    for item in a:
        res = re.split(r':', item, 1)
        # print(res)
        if len(res) < 2:
            retDict['RetName'] = res[0]
        else:
            retDict[res[0]] = res[1]
    meetInfo = re.split('\|', retDict['MeetPara'])
    for item in meetInfo:
        # print(item)
        deep1 = re.split(r';', item)
        # print("deep1: ",deep1)
        for itemD1 in deep1:
            deep2 = re.split(r'\=', itemD1, 1)
            # print(deep2)
            if deep2[0] in retDict and len(deep2) > 1:
                retDict[deep2[0]].append(deep2[1])
            elif len(deep2) > 1:
                retDict[deep2[0]] = []
                retDict[deep2[0]].append(deep2[1])
    return retDict


def brokenpipeHandle():
    pass


def makeConnection():
    global tcpCliSock

    global recvDict

    if tcpCliSock is not None:
        tcpCliSock.close()
    tcpCliSock = None
    while tcpCliSock is None:
        try:
            tcpCliSock = socket(AF_INET, SOCK_STREAM)
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

def setmeetgeneraparaTask(meetName="", meetMode="0", meetType="0"):
    print("running task")
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("setmeetgenerapara task")
    try:
        tcpCliSock.send((
                                "SETMEETGENERALPARA\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMeetMode:%s\r\nMeetType:%s\r\n\r\n" % (
                            seqNumber, meetName, meetMode, meetType)).encode('gb2312'))
        time.sleep(0.2)
        key = "SeqNumber:" + unicode(seqNumber)
        for i in range(0, 5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        return data
    # # 开始连接成功，后来MCU断开连接了
    # except ConnectionResetError as e:
    #     print("ConnectionResetError error: ", e)
    #
    # # 没连接到MCU
    # except BrokenPipeError as e:
    #     print("BrokenPipeError: ", e)

    except IOError as e:
        print("ioerror:", e)
        return None
    except BaseException as e:
        print("BaseException: ", e)


def addmeetTask(meetName="", meetAlias="", meetRemark=""):
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if meetName is "":
        return "param error"
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("addmeetTask task")
    try:
        tcpCliSock.send((
                                "ADDMEET\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMeetAlias:%s\r\nMeetRemark:%s\r\n\r\n" % (
                            seqNumber, meetName, meetAlias, meetRemark)).encode('gb2312'))
        time.sleep(0.2)
        key = "SeqNumber:" + unicode(seqNumber)
        for i in range(0, 5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:
                return data
        return data
    # # 开始连接成功，后来MCU断开连接了
    # except ConnectionResetError as e:
    #     print("ConnectionResetError error: ", e)
    #
    #
    # # 没连接到MCU
    # except BrokenPipeError as e:
    #     print("BrokenPipeError: ", e)

    except IOError as e:
        print("ioerror:", e)
        return None
    except BaseException as e:
        print("BaseException: ", e)


def deletemeetTask(meetName=""):
    global tcpCliSock
    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)
    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("deletemeetTask task")
    try:
        tcpCliSock.send(
            ("DELETEMEET\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\n\r\n" % (seqNumber, meetName)).encode('gb2312'))
        time.sleep(0.5)
        key = "SeqNumber:" + unicode(seqNumber)
        for i in range(0, 5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:
                return data
        return None
    # # 开始连接成功，后来MCU断开连接了
    # except ConnectionResetError as e:
    #     print("ConnectionResetError error: ", e)
    #     #
    # # 没连接到MCU
    # except BrokenPipeError as e:
    #     print("BrokenPipeError: ", e)

    except IOError as e:
        print("ioerror:", e)
    except BaseException as e:
        print("BaseException: ", e)
        #


def listmeetTask():
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("listmeetTask task")
    try:
        tcpCliSock.send(("LISTMEET\r\nVersion:1\r\nSeqNumber:%d\r\n\r\n" % seqNumber).encode('gb2312'))
        time.sleep(0.2)
        key = "SeqNumber:" + unicode(seqNumber)
        for i in range(0, 5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("BaseException: ", e)
        tcpCliSock = None


def addmemberTask(meetName="", memberName="0", memberIP="0"):
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("addmemberTask task")
    try:
        msg = (
                "ADDMEMBER\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\nMemberIP:%s\r\nMemberE164Alias:%s\r\nMemberH232Alias:%s\r\n\r\n" \
                % (seqNumber, meetName, memberName, memberIP, memberName, memberName))
        # print(msg)
        tcpCliSock.send(msg.encode('gb2312'))
        time.sleep(0.2)
        key = "SeqNumber:" + unicode(seqNumber)
        for i in range(0, 5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("BaseException: ", e)
        tcpCliSock = None
        return None


def setmemberavformatparaTask(meetName="", memberName="0", capalityName="1080P"):
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("addmemberTask task")
    try:
        msg = (
                "SETMEMBERAVFORMATPARA\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r"
                "\nCapabilityName:%s\r\n\r\n"
                % (seqNumber, meetName, memberName, capalityName))
        # print(msg)
        tcpCliSock.send(msg.encode('gb2312'))
        time.sleep(0.2)
        key = "SeqNumber:" + unicode(seqNumber)
        for i in range(0, 5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("BaseException: ", e)
        tcpCliSock = None
        return None


def callmemberTask(meetName="", memberName="0"):
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("callmemberTask task")
    try:
        msg = ("CALLMEMBER\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\n\r\n" \
               % (seqNumber, meetName, memberName))
        # print(msg)
        tcpCliSock.send(msg.encode('gb2312'))
        time.sleep(0.2)
        key = "SeqNumber:" + unicode(seqNumber)
        for i in range(0, 5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("callmemberTask BaseException: ", e)
        tcpCliSock = None
        return None


def set_gk_task(usegk=False, gk_ip="192.168.1.1"):
    print("set_gk_task", usegk, gk_ip)
    global tcpCliSock
    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    try:
        msg = ("SETGATEKEEPERPARA\r\nVersion:1\r\nSeqNumber:%d\r\nGKUseGK:%d\r\nGKIPAddr:%s\r\n\r\n"
               % (seqNumber, usegk, gk_ip))
        # print(msg)
        tcpCliSock.send(msg.encode('gb2312'))
        time.sleep(0.2)
        key = "SeqNumber:" + unicode(seqNumber)
        for i in range(0, 5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:
                return data
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("set_gk_task BaseException: ", e)
        tcpCliSock = None
        return None


def get_gk_status_task():
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("get_gk_status_task task")
    try:
        msg = ("GETGATEKEEPERPARA\r\nVersion:1\r\nSeqNumber:%d\r\n\r\n"
               % seqNumber)
        tcpCliSock.send(msg.encode('gb2312'))
        time.sleep(0.2)
        key = "SeqNumber:" + unicode(seqNumber)

        for i in range(0, 5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1 + i / 10)
                print(key, "-----------wait for cache in get_gk_status_task-------------")
                continue
            else:
                # print(data)
                return data
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("getmeetinfoTask BaseException: ", e)
        tcpCliSock = None
        return None


def checkNet():
    print("checkNet!")
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is not None:
        try:
            tcpCliSock.send(("HEARTBEAT\r\nVersion:1\r\nSeqNumber:%d\r\n\r\n" % seqNumber).encode('gb2312'))
            time.sleep(0.2)
            key = "SeqNumber:" + unicode(seqNumber)
            for i in range(0, 5):
                data = cache.get(key)
                if data is None:
                    time.sleep(0.1)
                    continue
                else:
                    # print("checknet ",data)
                    return data
            return None
        except BaseException as e:
            print("schedule error: ", e)
            tcpCliSock.close()
            tcpCliSock = socket(AF_INET, SOCK_STREAM)
            tcpCliSock.connect(ADDR)
            return "error"
    else:
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

        return "error"


def addavformatpara(meetname='', capalityname='', callbandwidth='', audioprotocol='', videoprotocol='', videoformat='',
                    videoframerate=60):
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("addavformatpara task")
    try:
        msg = (
                "ADDAVFORMATPARA\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nCapabilityName:%s\r\nCallBandWidth:%s\r\nAudioProtocol:%s\r\nVideoProtocol:%s\r\nVideoFormat:%s\r\nVideoFrameRate:%d\r\n\r\n" \
                % (seqNumber, meetname, capalityname, callbandwidth, audioprotocol, videoprotocol, videoformat,
                   videoframerate)).encode('gb2312')
        tcpCliSock.send(msg)
        time.sleep(0.2)
        key = "SeqNumber:" + unicode(seqNumber)
        for i in range(0, 5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("BaseException: ", e)
        tcpCliSock = None
        return None


def setdualformatparaTask(meetname="", dualprotocol='', dualformat='', dualBandWidth=1024):
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("setdualformatparaTask task")
    try:
        msg = (
                "SETDUALFORMATPARA\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nDualProtocol:%s\r\nDualFormat:%s\r\nDualBandWidth:%d\r\n\r\n" \
                % (seqNumber, meetname, dualprotocol, dualformat, dualBandWidth)).encode('gb2312')
        tcpCliSock.send(msg)
        time.sleep(0.2)
        key = "SeqNumber:" + unicode(seqNumber)
        for i in range(0, 5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("setdualformatparaTask BaseException: ", e)
        tcpCliSock = None
        return None


def getmeetinfoTask(meetName=""):
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("getmeetinfoTask task")
    try:
        msg = ("GETMEETINFO\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\n\r\n" \
               % (seqNumber, meetName))
        tcpCliSock.send(msg.encode('gb2312'))
        time.sleep(0.2)
        key = "SeqNumber:" + unicode(seqNumber)

        for i in range(0, 5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1 + i / 10)
                print(key, "-----------wait for cache in getmeetinfotask-------------")
                continue
            else:
                # print(data)
                return data
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("getmeetinfoTask BaseException: ", e)
        tcpCliSock = None
        return None


def hungupmemberTask(meetname, membername):
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("hungupmemberTask task")
    try:
        msg = ("HUNGUPMEMBER\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\n\r\n" \
               % (seqNumber, meetname, membername)).encode('gb2312')
        tcpCliSock.send(msg)
        time.sleep(0.2)
        key = "SeqNumber:" + unicode(seqNumber)
        for i in range(0, 5):
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
        print("hungupmemberTask BaseException: ", e)
        tcpCliSock = None
        return None


def mutememberTask(meetname, membername, isMuting=0):
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("mutememberTask task")
    try:
        msg = (
                "SETMEMBERAUDIOMUTING\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\nMutingMode:%d\r\n\r\n" \
                % (seqNumber, meetname, membername, isMuting)).encode('gb2312')
        # print(msg)
        tcpCliSock.send(msg)
        time.sleep(0.2)
        key = "SeqNumber:" + unicode(seqNumber)
        for i in range(0, 5):
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
        print("hungupmemberTask BaseException: ", e)
        tcpCliSock = None
        return None


def audioblockTask(meetname, membername, isBlock=0):
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("audioblockTask task")
    try:
        msg = (
                "SETMEMBERAUDIOBLOCKING\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r"
                "\nBlockingMode:%d\r\n\r\n"
                % (seqNumber, meetname, membername, isBlock)).encode('gb2312')
        tcpCliSock.send(msg)
        time.sleep(0.2)
        key = "SeqNumber:" + unicode(seqNumber)
        for i in range(0, 5):
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
        print("audioblockTask BaseException: ", e)
        tcpCliSock = None
        return None


def setcontrolmodeTask(meetname, membername, mode=0):
    global tcpCliSock

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("setcontrolmodeTask task")
    try:
        msg = ("MEETCONTROL\r\nMeetName:%s\r\nConMode:%d\r\nMemberName:%s\r\n\r\n" \
               % (meetname, int(mode), membername)).encode('gb2312')
        print(msg)
        tcpCliSock.send(msg)
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("setcontrolmodeTask BaseException: ", e)
        tcpCliSock = None
        return None


def getmemberinfoTask(meetname, membername):
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("getmemberinfoTask task")
    try:
        msg = ("GETMEMBERINFO\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\n\r\n" \
               % (seqNumber, meetname, membername)).encode('gb2312')
        tcpCliSock.send(msg)
        time.sleep(0.05)
        key = "SeqNumber:" + unicode(seqNumber)
        for i in range(0, 5):
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
        print("getmemberinfoTask BaseException: ", e)
        tcpCliSock = None
        return None


def deletememberTask(meetname, membername):
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("deletememberTask task")
    try:
        msg = ("DELETEMEMBER\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\n\r\n" \
               % (seqNumber, meetname, membername)).encode('gb2312')
        # print(msg)
        tcpCliSock.send(msg)
        time.sleep(0.2)
        key = "SeqNumber:" + unicode(seqNumber)
        for i in range(0, 5):
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
        print("deletememberTask BaseException: ", e)
        tcpCliSock = None
        return None


def setsecondvideosrcTask(meetname, membername, isSecond=0):
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("setsecondvideosrcTask task")
    try:
        msg = ("SETSECONDVIDEOSRC\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\nSwitcher:%d\r\n\r\n" \
               % (seqNumber, meetname, membername, isSecond)).encode('gb2312')
        # print(msg)
        tcpCliSock.send(msg)
        time.sleep(0.1)
        key = "SeqNumber:" + unicode(seqNumber)
        for i in range(0, 5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        print("setsecondvideosrcTask return None")
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("hungupmemberTask BaseException: ", e)
        tcpCliSock = None
        return None


# 这个函数只有主会场用
def setmemberidentityTask(meetname, membername):
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("setmemberidentityTask task")
    try:
        msg = ("SETMEMBERIDENTITY\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nMemberName:%s\r\n\r\n" \
               % (seqNumber, meetname, membername)).encode('gb2312')
        # print(msg)
        tcpCliSock.send(msg)
        time.sleep(0.1)
        key = "SeqNumber:" + unicode(seqNumber)
        for i in range(0, 5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:

                return data
        print("setmemberidentityTask return None")
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("setmemberidentityTask BaseException: ", e)
        tcpCliSock = None
        return None


#
def setmemberidentity_compTask(meetname, lecturename, audiencename):
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("setmemberidentity_compTask task")
    try:
        msg = (
                "SETMEMBERIDENTITY_COMP\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\nLectureName:%s\r\nAudienceName:%s\r\n\r\n" \
                % (seqNumber, meetname, lecturename, audiencename)).encode('gb2312')
        tcpCliSock.send(msg)
        time.sleep(0.1)
        key = "SeqNumber:" + unicode(seqNumber)
        for i in range(0, 5):
            data = cache.get(key)
            if data is None:
                time.sleep(0.1)
                continue
            else:
                return data
        print("setmemberidentity_compTask return None")
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("setmemberidentity_compTask BaseException: ", e)
        tcpCliSock = None
        return None


def hungallTask(meetname):
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("hungallTask task")
    try:
        msg = ("HUNGUPALL\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\n\r\n" \
               % (seqNumber, meetname)).encode('gb2312')
        tcpCliSock.send(msg)
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("hungallTask BaseException: ", e)
        tcpCliSock = None
        return None


def callallTask(meetname):
    global tcpCliSock

    seqNumber = cache.get('seqNumber')
    if seqNumber is None:
        seqNumber = 0
    cache.set('seqNumber', seqNumber + 1)

    if tcpCliSock is None:
        print("tcpCliSock is None")
        tcpCliSock = socket(AF_INET, SOCK_STREAM)
        tcpCliSock.connect(ADDR)

    print("callallTask task")
    try:
        msg = ("CALLALL\r\nVersion:1\r\nSeqNumber:%d\r\nMeetName:%s\r\n\r\n" \
               % (seqNumber, meetname)).encode('gb2312')
        tcpCliSock.send(msg)
        return None
    # 开始连接成功，后来MCU断开连接了
    except BaseException as e:
        print("callallTask BaseException: ", e)
        tcpCliSock = None
        return None


# ------------------------------------------------------------------------

def syncMeetingListAndDB(result):
    meeting.objects.all().update(activeInMcu=False)
    meetingNumber = result['MeetCount']
    # print(result)
    for index in range(0, int(meetingNumber)):
        filtered = meeting.objects.filter(name=result['MeetName'][index], meetcode=result['MeetAlias'][index])
        if filtered.exists():
            print("esists!")
            filtered.update(activeInMcu=True)
    meeting.objects.filter(activeInMcu=False).delete()


def analysisMeetinfo(retCode):
    if type(retCode) is not unicode:
        return False
    s = re.sub(r'\r\n\r\n', '', retCode)
    a = s.split('\r\n')
    retDict = {}
    for item in a:
        res = re.split(r':', item, 1)
        # print(res)
        if len(res) < 2:
            retDict['RetName'] = res[0]
        else:
            retDict[res[0]] = res[1]
    meetInfo = re.split('\|', retDict['MemberList'])
    for item in meetInfo:
        # print(item)
        deep1 = re.split(r';', item)
        # print("deep1: ",deep1)
        for itemD1 in deep1:
            deep2 = re.split(r'\=', itemD1, 1)
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
                data = addmeetTask(meetName, MeetAlias, meetRemark)
                # print("addmeetTask result:",data)
            except BaseException as e:
                print("timeout error: ", e)
                msgType = 'error'
                msg = "操作：添加会议，连接MCU超时"
                meetinglist = meeting.objects.all()
                return render(request, 'fun/meetinglist.html',
                              {'meetinglist': meetinglist, 'msgType': msgType, 'msg': msg})

            try:
                data = setmeetgeneraparaTask(meetName)
                # print("setmeetgeneraparaTask result:",data)
            except BaseException as e:
                print("setmeetgeneraparaTask timeout error: ", e)
                msgType = 'error'
                msg = "操作：设置会议参数，连接MCU超时"
                meetinglist = meeting.objects.all()
                return render(request, 'fun/meetinglist.html',
                              {'meetinglist': meetinglist, 'msgType': msgType, 'msg': msg})

            result = addavformatpara(meetName, capalityname, bandwidth, audioprotocol, videoprotocol, capalityname,
                                     videoframerate)
            try:
                data = result
                retDict = returnCode2Dict(data)
                if retDict['RetCode'] == "200":
                    print("addavformatparaTask return 200ok")
            except BaseException as e:
                print("addavformatparaTask timeout error: ", e)
                msgType = 'error'
                msg = "操作：设置会议格式参数，连接MCU超时"
                meetinglist = meeting.objects.all()
                return render(request, 'fun/meetinglist.html',
                              {'meetinglist': meetinglist, 'msgType': msgType, 'msg': msg})

            result = setdualformatparaTask(meetName, dualProtocol, dualFormat, dualBandWidth)
            try:
                data = result
                retDict = returnCode2Dict(data)
                if retDict['RetCode'] == "200":
                    print("setdualformatparaTask return 200ok")
                    return redirect(meetinglistView)
            except BaseException as e:
                print("setdualformatparaTask timeout error: ", e)
                msgType = 'error'
                msg = "操作：设置会议双流参数，连接MCU超时"
                meetinglist = meeting.objects.all()
                return render(request, 'fun/meetinglist.html',
                              {'meetinglist': meetinglist, 'msgType': msgType, 'msg': msg})
            return redirect(meetinglistView)
        else:
            e164name = getmcue164()
            msg = u"填写错误，请重新提交!" + u" 如果级联会议，请将会议名称改写为：" + e164name + "1"
            return render(request, 'fun/creat_meeting.html',
                          {'meetform': meetform, 'msgType': "error", 'msg': msg})
    else:
        meetform = meetingForm()
        e164name = getmcue164()
        msg = u"请添加会议" + u" 如果级联会议，请将会议名称改写为：" + e164name + "1"
        return render(request, 'fun/creat_meeting.html', {'meetform': meetform, 'msgType': "info",
                                                          'msg': msg})


@login_required
def delete_meetingView(request, meetpk):
    if not meeting.objects.filter(pk=meetpk).exists():
        print("该会议不存在！")
        msgType = "error"
        msg = "该会议不存在"
        meetinglist = meeting.objects.all()
        return render(request, 'fun/meetinglist.html', {'meetinglist': meetinglist, 'msgType': msgType, 'msg': msg})
    else:
        meet = meeting.objects.get(pk=meetpk)
        meetname = meet.name

        try:
            # hungallTask(meetname)
            # time.sleep(0.2)

            # result = getmeetinfoTask(meetname)
            # notifyList = cache.get('notify')
            # if notifyList is not None:
            #     # print(notifyList)
            #     for notify in notifyList:
            #         if 'RESP_NOTIFYONLINE' in  notify:
            #             if ('MeetName:%s' % meetname) in notify and ('MemberName:%s' % mainMeetRoomName) in notify:
            #                 print("mainMeetRoom online!!!!!!!!!")
            #                 setmemberidentityTask(meetname,mainMeetRoomName)
            #     cache.delete('notify')
            # # print("getmeetinfo result is: \n",result)
            # if result is not None:
            #     analysysResult = analysisMeetinfo(result)
            #     # analysysResult['']
            #     if "EPName" in analysysResult.keys():
            #         analysysResult['pk'] = []
            #         for ename in analysysResult['EPName']:
            #             if terminal.objects.filter(name = ename).exists():
            #                 analysysResult['pk'].append(terminal.objects.get(name = ename).pk)
            #             else:
            #                 analysysResult['pk'].append("None")
            #     # print(analysysResult)
            #     return HttpResponse(json.dumps(analysysResult))
            # else:
            #     print("--------------------------------------------")

            result = getmeetinfoTask(meetname)
            print(meetname, " getmeetinfoTask return: ", result)

            if result is not None:
                analysysResult = analysisMeetinfo(result)
                print(analysysResult)

            else:
                msgType = "error"
                msg = "获取会议信息失败"
                meetinglist = meeting.objects.all()
                return render(request, 'fun/meetinglist.html',
                              {'meetinglist': meetinglist, 'msgType': msgType, 'msg': msg})

            if 'MemberState' in analysysResult.keys() and (
                    '1' in analysysResult['MemberState'] or '2' in analysysResult['MemberState']):
                print("还有终端没挂断！")
                msgType = "error"
                msg = "存在未挂断的终端，请进入会控页面挂断"
                meetinglist = meeting.objects.all()
                return render(request, 'fun/meetinglist.html',
                              {'meetinglist': meetinglist, 'msgType': msgType, 'msg': msg})

            else:
                result = deletemeetTask(meetname)
                notifyList = cache.get('notify')
                if notifyList is not None:
                    # # print(notifyList)
                    cache.delete('notify')
                if result is None:
                    meeting.objects.get(pk=meetpk).delete()
                    msgType = "error"
                    msg = "删除失败"
                    meetinglist = meeting.objects.all()
                    return render(request, 'fun/meetinglist.html',
                                  {'meetinglist': meetinglist, 'msgType': msgType, 'msg': msg})

            meeting.objects.get(pk=meetpk).delete()
            msgType = "success"
            msg = "删除成功"
            meetinglist = meeting.objects.all()
            return render(request, 'fun/meetinglist.html', {'meetinglist': meetinglist, 'msgType': msgType, 'msg': msg})
        except BaseException as e:
            print("delete_meetingView error:", e)

            meeting.objects.get(pk=meetpk).delete()
            msgType = "error"
            msg = "删除失败1"
            meetinglist = meeting.objects.all()
            return render(request, 'fun/meetinglist.html', {'meetinglist': meetinglist, 'msgType': msgType, 'msg': msg})


@login_required
def meetinglistView(request, msgType='', msg=''):
    try:
        data = listmeetTask()
        print(data)
    except BaseException as e:
        print("timeout error: ", e)
        msgType = "error"
        msg = "连接MCU失败，显示数据库备份内容"
        meetinglist = meeting.objects.all()
        return render(request, 'fun/meetinglist.html', {'meetinglist': meetinglist, 'msgType': msgType, 'msg': msg})
    if not data:
        msgType = "error"
        msg = "连接MCU失败，显示数据库备份内容"
        meetinglist = meeting.objects.all()
        return render(request, 'fun/meetinglist.html', {'meetinglist': meetinglist, 'msgType': msgType, 'msg': msg})
    result = analysisListMeetResult(data)
    print("---", result)
    syncMeetingListAndDB(result)
    msgType = "nothing"
    msg = "未知连接错误，将显示数据库备份内容"
    meetinglist = meeting.objects.all()
    return render(request, 'fun/meetinglist.html', {'meetinglist': meetinglist, 'msgType': msgType, 'msg': msg})


# @login_required
# def meetinglistView(request):
#     return render(request,'meeting_manage/meetinglist.html')

@login_required
def terminallistView(request, msgType='', msg=''):
    terminalList = terminal.objects.all()
    return render(request, 'fun/terminallist.html', {'terminallist': terminalList, 'msgType': msgType, 'msg': msg})


@login_required
def addterminalView(request):
    if request.POST:
        terminalform = terminalForm(request.POST)
        if terminalform.is_valid():
            terminalform.save(commit=True)
            terminalList = terminal.objects.all()
            # return HttpResponseRedirect('/terminallist',msg="1234")
            # return HttpResponseRedirect(reverse('terminallist', kwargs={'msg': 'auth'}))
            return terminallistView(request, "success", "add success!")
            return render(request, 'fun/terminallist.html',
                          {'terminallist': terminalList, 'msgType': 'success', 'msg': "add success!!!!"})
        else:
            return render(request, 'fun/addterminal.html',
                          {'terminalform': terminalform, 'msgType': 'error', 'msg': "fail to add"})
    else:
        terminalform = terminalForm()
        return render(request, 'fun/addterminal.html',
                      {'terminalform': terminalform, 'msgType': 'info', 'msg': "please add"})


@login_required
def deleteterminalView(request, terminalpk):
    if not terminal.objects.filter(pk=terminalpk).exists():
        print("该终端不存在！")
        msgType = "error"
        msg = "该终端不存在"
        terminalList = terminal.objects.all()
        return render(request, 'fun/terminallist.html', {'terminallist': terminalList, 'msgType': 'info', 'msg': msg})
    else:
        terminal.objects.get(pk=terminalpk).delete()
        terminalList = terminal.objects.all()
        msgType = "success"
        msg = "删除成功"
        return render(request, 'fun/terminallist.html', {'terminallist': terminalList, 'msgType': 'info', 'msg': msg})


@login_required
def terminallistViewP(request, msg):
    terminalList = terminal.objects.all()
    return render(request, 'fun/terminallist.html', {'terminallist': terminalList, 'msgType': 'info', 'msg': msg})


@login_required
def templatelistView(request, msgType='', msg=''):
    templateList = meetingTemplate.objects.all()
    return render(request, 'fun/templatelist.html', {'templatelist': templateList, 'msgType': msgType, 'msg': msg})


@login_required
def addtemplateView(request):
    if request.POST:
        templateform = meetingTemplateForm(request.POST)
        if templateform.is_valid():
            templateform.save(commit=True)
            templateList = meetingTemplate.objects.all()
            return render(request, 'fun/templatelist.html',
                          dict(templatelist=templateList, msgType='success', msg=u'添加成功'))
        else:
            return render(request, 'fun/addtemplate.html',
                          dict(templateform=templateform, msgType='error', msg=u"添加失败，请检查"))
    else:
        templateform = meetingTemplateForm()
        return render(request, 'fun/addtemplate.html',
                      dict(templateform=templateform, msgType='info', msg=_(u"请添加")))


@login_required
def deletetemplateView(request, templatepk):
    if not meetingTemplate.objects.filter(pk=templatepk).exists():
        print("该模板不存在！")
        msgType = "error"
        msg = "该模板不存在"
        templateList = meetingTemplate.objects.all()
        return render(request, 'fun/templatelist.html', {'templatelist': templateList, 'msgType': msgType, 'msg': msg})
    else:
        meetingTemplate.objects.get(pk=templatepk).delete()
        templateList = meetingTemplate.objects.all()
        return render(request, 'fun/templatelist.html',
                      {'templatelist': templateList, 'msgType': 'success', 'msg': '删除成功'})


# Ajax Views
# ---------------------------------------------------------------------------

@login_required
def heartBeatAjaxView(request):
    if request.is_ajax():
        print("recv heartBeat ajax request")
        result = ""
        try:
            result = checkNet()
            if result is None:
                return HttpResponse(False)
            # print("heart beat check result is: \n",result)
        except BaseException as e:
            print("catch heartbeat error", e)
            return HttpResponse(False)
        return HttpResponse(True)


@login_required
def callmemberAjaxView(request, meetpk, pk):
    if request.is_ajax():
        print("recv callmember ajax request")
        result = ""
        if not meeting.objects.filter(pk=meetpk).exists():
            print("该会议不存在！")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "该会议不存在！"}))
        if not terminal.objects.filter(pk=pk).exists():
            print("该终端不存在！")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "该终端不存在！"}))
        meetname = meeting.objects.get(pk=meetpk).name
        membername = terminal.objects.get(pk=pk).name
        memberip = terminal.objects.get(pk=pk).terminalIP

        capability = terminal.objects.get(pk=pk).capalityname
        # add member
        try:
            result = addmemberTask(meetname, membername, memberip)
            time.sleep(0.1)
            result = setmemberavformatparaTask(meetname, membername, capability)
            time.sleep(0.1)
            result = callmemberTask(meetname, membername)
        #     # print("add member check result is: \n",result)
        # except BaseException as e:
        #     print("catch add member error",e)
        #     return HttpResponse(json.dumps({'msgType':"error",'msg':"向会议中添加终端过程中发生通信错误！"}))
        # if result is None:
        #     print("add member return None")
        #     return HttpResponse(json.dumps({'msgType':"error",'msg':"向会议中添加终端过程中MCU返回None！"}))
        # retDict = returnCode2Dict(result)
        # if retDict['RetCode'] != "200":
        #     # print("addmemberTask return %s" % retDict['RetCode'])
        #     return HttpResponse(json.dumps({'msgType':"error",'msg':("向会议中添加终端过程中MCU返回%s！" % retDict['RetCode'])}))
        # # setmemberavformatpara
        # try:
        #     result = setmemberavformatparaTask(meetname,membername,capability)
        #     # print("setmemberavformatpara check result is: \n",result)
        # except BaseException as e:
        #     print("catch setmemberavformatpara error",e)
        #     return HttpResponse(json.dumps({'msgType':"error",'msg':"向会议中添加终端参数过程中发生通信错误！"}))
        # if result is None:
        #     print("setmemberavformatpara return None")
        #     return HttpResponse(json.dumps({'msgType':"error",'msg':"向会议中添加终端参数过程中MCU返回None！"}))
        # retDict = returnCode2Dict(result)
        # if retDict['RetCode'] != "200":
        #     print("setmemberavformatpara return %s" % retDict['RetCode'])
        #     return HttpResponse(json.dumps({'msgType':"error",'msg':("向会议中添加终端参数过程中MCU返回%s！" % retDict['RetCode'])}))
        # # callmember
        # try:
        #     result = callmemberTask(meetname,membername)
        # print("callmemberTask result is: \n",result)
        except BaseException as e:
            print("catch callmemberTask error", e)
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "呼叫终端过程中发生通信错误！"}))
        if result is None:
            print("callmemberTask return None")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "呼叫终端过程中MCU返回None！"}))
        retDict = returnCode2Dict(result)
        if retDict['RetCode'] != "200":
            # print("callmemberTask return %s" % retDict['RetCode'])
            return HttpResponse(json.dumps({'msgType': "error", 'msg': ("呼叫终端过程中MCU返回%s！" % retDict['RetCode'])}))
        # time.sleep(0.5)
        # 设为主会场

        if pk == meeting.objects.get(pk=meetpk).mainMeetRoom:
            print("这是大哥！！")
            try:
                time.sleep(0.3)
                result = setmemberidentityTask(meetname, membername)
            except BaseException as e:
                print("catch setmemberidentityTask error", e)
                return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置主会场过程中发生通信错误！"}))
            if result is None:
                print("callmemberTask return None")
                return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置主会场过程中MCU返回None！"}))
            retDict = returnCode2Dict(result)
            if retDict['RetCode'] != "200":
                # print("callmemberTask return %s" % retDict['RetCode'])
                return HttpResponse(json.dumps({'msgType': "error", 'msg': ("设置主会场过程中MCU返回%s！" % retDict['RetCode'])}))
        print(pk, "is pk----------mainmeetroom is ", meeting.objects.get(pk=meetpk).mainMeetRoom)
        # getmemberinfoTask
        result = getmemberinfoTask(meetname, membername)
        # print("getmemberinfoTask return: ",result)
        if result is None:
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "getmemberinfoTask返回None！"}))
        retcode = returnCode2Dict(result)
        retcode["pk"] = pk
        return HttpResponse(json.dumps(retcode))
        # print(analysis(result))

        return HttpResponse(json.dumps({'msgType': "success", 'msg': "操作成功！"}))


@login_required
def getmeetinfoAjaxView(request, meetpk):
    if request.is_ajax():
        print("recv getmeetinfo ajax request")
        result = ""
        if not meeting.objects.filter(pk=meetpk).exists():
            print("该会议不存在！")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "该会议不存在！"}))

        meetname = meeting.objects.get(pk=meetpk).name
        mainMeetRoom = meeting.objects.get(pk=meetpk).mainMeetRoom
        if not terminal.objects.filter(pk=mainMeetRoom).exists():
            print("该会议不存在！")
            mainMeetRoomName = None
        else:
            mainMeetRoomName = terminal.objects.get(pk=mainMeetRoom).name
        # getmeetinfo
        try:

            result = getmeetinfoTask(meetname)
            notifyList = cache.get('notify')
            if notifyList is not None:
                # print(notifyList)
                # for notify in notifyList:
                #     if 'RESP_NOTIFYONLINE' in  notify:
                #         if ('MeetName:%s' % meetname) in notify and ('MemberName:%s' % mainMeetRoomName) in notify:
                #             print("mainMeetRoom online!!!!!!!!!")
                #             setmemberidentityTask(meetname,mainMeetRoomName)
                cache.delete('notify')
            # print("getmeetinfo result is: \n",result)
            if result is not None:
                analysysResult = analysisMeetinfo(result)
                # analysysResult['']
                if "EPName" in analysysResult.keys():
                    analysysResult['pk'] = []
                    for ename in analysysResult['EPName']:
                        if terminal.objects.filter(name=ename).exists():
                            analysysResult['pk'].append(terminal.objects.get(name=ename).pk)
                        else:
                            analysysResult['pk'].append("None")
                # print(analysysResult)
                return HttpResponse(json.dumps(analysysResult))
        except BaseException as e:
            print("catch getmeetinfo error", e, "-----", result)
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "获取会议信息过程中发生通信错误！"}))
        if result is None:
            print("getmeetinfo return None")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "获取会议信息过程中MCU返回None！"}))
        retDict = returnCode2Dict(result)
        if retDict['RetCode'] != "200":
            # print("getmeetinfo return %s" % retDict['RetCode'])
            return HttpResponse(json.dumps({'msgType': "error", 'msg': ("获取会议信息过程中MCU返回%s！" % retDict['RetCode'])}))
        return HttpResponse(json.dumps({'msgType': "success", 'msg': "操作成功！"}))


@login_required
def hungupAjaxView(request, meetpk, pk):
    if request.is_ajax():
        print("recv hungupAjaxView ajax request")
        result = ""
        if not meeting.objects.filter(pk=meetpk).exists():
            print("该会议不存在！")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "该会议不存在！"}))
        if not terminal.objects.filter(pk=pk).exists():
            print("该终端不存在！")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "该终端不存在！"}))
        meetname = meeting.objects.get(pk=meetpk).name
        membername = terminal.objects.get(pk=pk).name
        memberip = terminal.objects.get(pk=pk).terminalIP
        # hungupAjaxView
        try:

            result = hungupmemberTask(meetname, membername)
            notifyList = cache.get('notify')
            if notifyList is not None:
                # # print(notifyList)
                cache.delete('notify')
            if result is None:
                return HttpResponse(json.dumps({'msgType': "error", 'msg': "挂断过程中MCU返回None！"}))
            result = deletememberTask(meetname, membername)
            notifyList = cache.get('notify')
            if notifyList is not None:
                # # print(notifyList)
                cache.delete('notify')
            if result is None:
                return HttpResponse(json.dumps({'msgType': "error", 'msg': "挂断过程中MCU返回None！"}))
            return HttpResponse(json.dumps({'msgType': "success", 'msg': "操作成功！"}))
        except BaseException as e:
            print("catch hungup error", e)
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "挂断过程中发生通信错误！"}))
        if result is None:
            print("hungup return None")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "挂断过程中MCU返回None！"}))
        retDict = returnCode2Dict(result)
        if retDict['RetCode'] != "200":
            # print("getmeetinfo return %s" % retDict['RetCode'])
            return HttpResponse(json.dumps({'msgType': "error", 'msg': ("挂断过程中MCU返回%s！" % retDict['RetCode'])}))
        return HttpResponse(json.dumps({'msgType': "success", 'msg': "操作成功！"}))


# 设置闭麦
@login_required
def silencememberAjaxView(request, meetpk, pk, mode):
    if request.is_ajax():
        print("recv silencememberAjaxView ajax request")
        result = ""
        if not meeting.objects.filter(pk=meetpk).exists():
            print("该会议不存在！")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "该会议不存在！"}))
        if not terminal.objects.filter(pk=pk).exists():
            print("该终端不存在！")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "该终端不存在！"}))
        meetname = meeting.objects.get(pk=meetpk).name
        membername = terminal.objects.get(pk=pk).name
        memberip = terminal.objects.get(pk=pk).terminalIP
        # hungupAjaxView
        try:

            result = mutememberTask(meetname, membername, int(mode))
            notifyList = cache.get('notify')
            if notifyList is not None:
                # # print(notifyList)
                cache.delete('notify')
            if result is None:
                return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置闭麦过程中MCU返回None！"}))
            # print("mutememberTask return: ",result)
            result = getmemberinfoTask(meetname, membername)

            notifyList = cache.get('notify')
            if notifyList is not None:
                pass
                # print(notifyList)
                # cache.delete('notify')
            if result is None:
                return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置闭麦过程中MCU返回None！"}))
            # print("getmemberinfoTask return: ",result)
            retcode = returnCode2Dict(result)
            retcode["pk"] = pk
            return HttpResponse(json.dumps(retcode))
        except BaseException as e:
            print("catch getmeetinfo error", e)
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置闭麦过程中发生通信错误！"}))
        if result is None:
            print("getmeetinfo return None")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置闭麦过程中MCU返回None！"}))
        retDict = returnCode2Dict(result)
        if retDict['RetCode'] != "200":
            # print("getmeetinfo return %s" % retDict['RetCode'])
            return HttpResponse(json.dumps({'msgType': "error", 'msg': ("设置闭麦过程中MCU返回%s！" % retDict['RetCode'])}))
        return HttpResponse(json.dumps({'msgType': "success", 'msg': "操作成功！"}))


# 设置静音
@login_required
def audioblockAjaxView(request, meetpk, pk, mode):
    if request.is_ajax():
        print("recv audioblockAjaxView ajax request")
        result = ""
        if not meeting.objects.filter(pk=meetpk).exists():
            print("该会议不存在！")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "该会议不存在！"}))
        if not terminal.objects.filter(pk=pk).exists():
            print("该终端不存在！")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "该终端不存在！"}))
        meetname = meeting.objects.get(pk=meetpk).name
        membername = terminal.objects.get(pk=pk).name
        memberip = terminal.objects.get(pk=pk).terminalIP
        # hungupAjaxView
        try:

            result = audioblockTask(meetname, membername, int(mode))
            notifyList = cache.get('notify')
            if notifyList is not None:
                # # print(notifyList)
                cache.delete('notify')
            if result is None:
                return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置静音过程中MCU返回None！"}))
            # print("mutememberTask return: ",result)
            result = getmemberinfoTask(meetname, membername)

            notifyList = cache.get('notify')
            if notifyList is not None:
                pass
                # print(notifyList)
                # cache.delete('notify')
            if result is None:
                return HttpResponse(json.dumps({'msgType': "error", 'msg': "禁言过程中MCU返回None！"}))
            # print("getmemberinfoTask return: ",result)
            retcode = returnCode2Dict(result)
            retcode["pk"] = pk
            return HttpResponse(json.dumps(retcode))
        except BaseException as e:
            print("catch getmeetinfo error", e)
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "禁言过程中发生通信错误！"}))
        if result is None:
            print("getmeetinfo return None")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "禁言过程中MCU返回None！"}))
        retDict = returnCode2Dict(result)
        if retDict['RetCode'] != "200":
            # print("getmeetinfo return %s" % retDict['RetCode'])
            return HttpResponse(json.dumps({'msgType': "error", 'msg': ("禁言过程中MCU返回%s！" % retDict['RetCode'])}))
        return HttpResponse(json.dumps({'msgType': "success", 'msg': "操作成功！"}))


# 设置双流
@login_required
def setsecondvideosrcAjaxView(request, meetpk, pk, mode):
    if request.is_ajax():
        print("recv setsecondvideosrcAjaxView ajax request")
        result = ""
        if not meeting.objects.filter(pk=meetpk).exists():
            print("该会议不存在！")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "该会议不存在！"}))
        if not terminal.objects.filter(pk=pk).exists():
            print("该终端不存在！")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "该终端不存在！"}))
        meetname = meeting.objects.get(pk=meetpk).name
        membername = terminal.objects.get(pk=pk).name
        memberip = terminal.objects.get(pk=pk).terminalIP
        # hungupAjaxView
        try:

            result = setsecondvideosrcTask(meetname, membername, int(mode))
            notifyList = cache.get('notify')
            if notifyList is not None:
                # # print(notifyList)
                cache.delete('notify')
            if result is None:
                return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置双流过程中MCU返回None！"}))
            # print("mutememberTask return: ",result)
            result = getmemberinfoTask(meetname, membername)

            notifyList = cache.get('notify')
            if notifyList is not None:
                pass
                # print(notifyList)
                # cache.delete('notify')
            if result is None:
                return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置双流过程中MCU返回None！"}))
            # print("getmemberinfoTask return: ",result)
            retcode = returnCode2Dict(result)
            retcode["pk"] = pk
            return HttpResponse(json.dumps(retcode))
        except BaseException as e:
            print("catch getmeetinfo error", e)
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置双流过程中发生通信错误！"}))
        if result is None:
            print("getmeetinfo return None")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置双流过程中MCU返回None！"}))
        retDict = returnCode2Dict(result)
        if retDict['RetCode'] != "200":
            # print("getmeetinfo return %s" % retDict['RetCode'])
            return HttpResponse(json.dumps({'msgType': "error", 'msg': ("设置双流过程中MCU返回%s！" % retDict['RetCode'])}))
        return HttpResponse(json.dumps({'msgType': "success", 'msg': "操作成功！"}))


@login_required
def seeAjaxView(request, meetpk, pk, mode):
    if request.is_ajax():
        print("recv seeAjaxView ajax request")
        result = ""
        if not meeting.objects.filter(pk=meetpk).exists():
            print("该会议不存在！")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "该会议不存在！"}))
        if not terminal.objects.filter(pk=pk).exists():
            print("该终端不存在！")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "该终端不存在！"}))
        meetname = meeting.objects.get(pk=meetpk).name
        membername = terminal.objects.get(pk=pk).name
        memberip = terminal.objects.get(pk=pk).terminalIP
        try:
            mainMeetRoomPK = meeting.objects.get(pk=meetpk).mainMeetRoom
            if not terminal.objects.filter(pk=mainMeetRoomPK).exists():
                print("主会场不存在")
                return HttpResponse(json.dumps({'msgType': "error", 'msg': "主会场不存在！"}))
            mainMeetRoomName = terminal.objects.get(pk=mainMeetRoomPK).name

            # 第二个参数是谁看被查看的对象，第三个参数是被看的是谁
            result = setmemberidentity_compTask(meetname, mainMeetRoomName, membername)
            notifyList = cache.get('notify')
            if notifyList is not None:
                # # print(notifyList)
                cache.delete('notify')
            if result is None:
                return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置查看过程中MCU返回None！"}))
            # print("mutememberTask return: ",result)
            result = getmemberinfoTask(meetname, membername)

            notifyList = cache.get('notify')
            if notifyList is not None:
                pass
                # print(notifyList)
                # cache.delete('notify')
            if result is None:
                return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置查看过程中MCU返回None！"}))
            # print("getmemberinfoTask return: ",result)
            retcode = returnCode2Dict(result)
            retcode["pk"] = pk
            return HttpResponse(json.dumps(retcode))
        except BaseException as e:
            print("catch seeAjaxView error", e)
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置查看过程中发生通信错误！"}))
        if result is None:
            print("getmeetinfo return None")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置查看过程中MCU返回None！"}))
        retDict = returnCode2Dict(result)
        if retDict['RetCode'] != "200":
            # print("getmeetinfo return %s" % retDict['RetCode'])
            return HttpResponse(json.dumps({'msgType': "error", 'msg': ("设置查看过程中MCU返回%s！" % retDict['RetCode'])}))
        return HttpResponse(json.dumps({'msgType': "success", 'msg': "操作成功！"}))


@login_required
def broadcastAjaxView(request, meetpk, pk, mode):
    if request.is_ajax():
        print("recv broadcastAjaxView ajax request")
        result = ""
        if not meeting.objects.filter(pk=meetpk).exists():
            print("该会议不存在！")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "该会议不存在！"}))
        if not terminal.objects.filter(pk=pk).exists():
            print("该终端不存在！")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "该终端不存在！"}))
        meetname = meeting.objects.get(pk=meetpk).name
        membername = terminal.objects.get(pk=pk).name
        memberip = terminal.objects.get(pk=pk).terminalIP
        try:
            mainMeetRoomPK = meeting.objects.get(pk=meetpk).mainMeetRoom
            if not terminal.objects.filter(pk=mainMeetRoomPK).exists():
                print("主会场不存在")
                return HttpResponse(json.dumps({'msgType': "error", 'msg': "主会场不存在！"}))
            mainMeetRoomName = terminal.objects.get(pk=mainMeetRoomPK).name

            # 第二个参数是谁看被查看的对象，第三个参数是被看的是谁
            result = setmemberidentity_compTask(meetname, membername, mainMeetRoomName)
            notifyList = cache.get('notify')
            if notifyList is not None:
                # # print(notifyList)
                cache.delete('notify')
            if result is None:
                return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置广播过程中MCU返回None！"}))
            # print("mutememberTask return: ",result)
            result = getmemberinfoTask(meetname, membername)

            notifyList = cache.get('notify')
            if notifyList is not None:
                pass
                # print(notifyList)
                # cache.delete('notify')
            if result is None:
                return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置广播过程中MCU返回None！"}))
            # print("getmemberinfoTask return: ",result)
            retcode = returnCode2Dict(result)
            retcode["pk"] = pk
            return HttpResponse(json.dumps(retcode))
        except BaseException as e:
            print("catch broadcastAjaxView error", e)
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置广播过程中发生通信错误！"}))


@login_required
def hungupallAjaxView(request, meetpk):
    if request.is_ajax():
        print("recv hungupallAjaxView ajax request")
        result = ""
        if not meeting.objects.filter(pk=meetpk).exists():
            print("该会议不存在！")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "该会议不存在！"}))

        meetname = meeting.objects.get(pk=meetpk).name

        try:
            result = getmeetinfoTask(meetname)
            if result is not None:
                analysysResult = analysisMeetinfo(result)
            else:
                print("NONE!!!!!!!!!!!!!")
            memberList = []
            if analysysResult is not None:
                memberList = analysysResult["EPName"]

            # hungallCeleryTask.apply_async((meetname, json.dumps(memberList)), serializer='json')
            thread1 = hangup_all(meetname, json.dumps(memberList))
            thread1.start()

            return HttpResponse(json.dumps({'msgType': "success", 'msg': "成功发送挂断所有消息，请耐心等待"}))
        except BaseException as e:
            print("catch hungupallAjaxView error", e)
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置挂断过程中发生通信错误！"}))


@login_required
def callallAjaxView(request, meetpk):
    if request.method == "POST" and request.is_ajax():
        print("recv callallAjaxView ajax request")
        result = ""
        if not meeting.objects.filter(pk=meetpk).exists():
            print("该会议不存在！")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "该会议不存在！"}))

        meetname = meeting.objects.get(pk=meetpk).name
        mainMeetRoomPK = meeting.objects.get(pk=meetpk).mainMeetRoom
        if not terminal.objects.filter(pk=mainMeetRoomPK).exists():
            print("主会场不存在")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "主会场不存在！"}))

        mainMeetRoomName = terminal.objects.get(pk=mainMeetRoomPK).name

        memberList = request.POST['checked']

        memberList = json.loads(memberList)

        if memberList is None:
            memberList = []
            return HttpResponse(json.dumps({'msgType': "success", 'msg': "成功发送呼叫所有消息，请耐心等待"}))
        if len(memberList) == 0:
            return HttpResponse(json.dumps({'msgType': "success", 'msg': "成功发送呼叫所有消息，请耐心等待"}))
        memberInfoList = []
        for member in memberList:
            pk = int(member)
            print(pk)
            if not terminal.objects.filter(pk=pk).exists():
                print("该终端不存在！")
                continue
            tmp = terminal.objects.get(pk=pk)
            tmpDict = {}
            tmpDict['name'] = tmp.name
            tmpDict['terminalIP'] = tmp.terminalIP
            tmpDict['capalityName'] = tmp.capalityname
            memberInfoList.append(tmpDict)

        jsonMemberInfoList = json.dumps(memberInfoList)
        print(jsonMemberInfoList)
        try:
            thread1 = call_all(meetname, mainMeetRoomName, jsonMemberInfoList)
            thread1.start()
            # callallCeleryTask.apply_async((meetname, mainMeetRoomName, jsonMemberInfoList), serializer='json')
            return HttpResponse(json.dumps({'msgType': "success", 'msg': "成功发送挂断所有消息，请耐心等待"}))
        except BaseException as e:
            print("catch callallAjaxView error", e)
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "设置挂断过程中发生通信错误！"}))


# ---------------------------------------------------------------------------

@login_required
def setoperationmodeAjaxView(request, meetpk, mode):
    if request.is_ajax():
        if not meeting.objects.filter(pk=meetpk).exists():
            print("该会议不存在！")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "该会议不存在！"}))
        meetInstance = meeting.objects.get(pk=meetpk)
        meetname = meetInstance.name

        mainMeetRoomPK = meeting.objects.get(pk=meetpk).mainMeetRoom
        if not terminal.objects.filter(pk=mainMeetRoomPK).exists():
            print("主会场不存在")
            return HttpResponse(json.dumps({'msgType': "error", 'msg': "主会场不存在！"}))
        mainMeetRoomName = terminal.objects.get(pk=mainMeetRoomPK).name

        if mode in ['0', '1', '2']:
            print("set operation model: ", mode)
            if mode == '0':
                setcontrolmodeTask(meetname, mainMeetRoomName, 0)
                meetInstance.operationModel = "操作员模式"
                meetInstance.save()
            if mode == '1':
                setcontrolmodeTask(meetname, mainMeetRoomName, 1)
                meetInstance.operationModel = "语音激励模式"
                meetInstance.save()
            if mode == '2':
                setcontrolmodeTask(meetname, mainMeetRoomName, 2)
                meetInstance.operationModel = "主席模式"
                meetInstance.save()
            return HttpResponse(json.dumps({'msgType': "success", 'msg': "操作成功！"}))
        else:
            setcontrolmodeTask(meetname, mainMeetRoomName, 0)
            meetInstance.operationModel = "操作员模式"
            meetInstance.save()
            return HttpResponse(json.dumps({'msgType': "success", 'msg': "操作成功！"}))


@login_required
def meetDetailsView(request, meetpk):
    if not meeting.objects.filter(pk=meetpk).exists():
        print("该会议不存在！")
        return redirect(meetinglistView)
    meetInstance = meeting.objects.get(pk=meetpk)
    terminalList = terminal.objects.all()
    return render(request, 'fun/meetDetail.html',
                  {'meetInstance': meetInstance, 'terminalList': terminalList, 'msgType': 'info', 'msg': "please add"})


def getmcue164():
    cf = ConfigParser.ConfigParser()
    mcue164name = ""
    try:
        # os.chdir("C:\SVCMMCUAutoStart")
        cf.read("C:\SVCMMCUAutoStart\svcmmcu.ini")
        mcue164name = cf.get("svcmmcu::gatekeeper", "Gatekeeper UserNamePrefix")
    except BaseException as e:
        print("getmcue164 error occurs: ", e)
    return mcue164name


def setmcue164(e164name):
    try:
        config = ConfigObj("C:\SVCMMCUAutoStart\svcmmcu.ini")
        config['svcmmcu::gatekeeper']['Gatekeeper UserNamePrefix'] = e164name.encode("gb2312")
        config.write()
    except BaseException as e:
        print("setmcue164 error occurs: ", e)



@login_required
def GK_configView(request):
    if request.POST:
        gk_form_data = gkForm(data=request.POST)
        if gk_form_data.is_valid():
            use_gk = gk_form_data.cleaned_data["active"]
            gk_addr = gk_form_data.cleaned_data["ip"]
            e164 = gk_form_data.cleaned_data["e164"]
            print("GK_configView", use_gk, gk_addr, e164)

            ret = set_gk_task(use_gk, gk_addr)
            ret_dict = returnCode2Dict(ret)
            if not ret_dict:
                return redirect(GK_configView)
            ret_code = ret_dict.get("RetCode", None)
            if e164 != getmcue164():
                setmcue164(e164)
                os.system('taskkill /f /im "SVCMMCU.exe"')
                time.sleep(2.5)
            if ret_code == "200":
                time.sleep(1.5)
                return redirect(GK_configView)
            return redirect(GK_configView)
        else:
            return render(request, 'system_manage/GK_config.html', {'form': gk_form_data})
    else:
        ret = get_gk_status_task()

        ret_dict = returnCode2Dict(ret)
        print("22222222", ret_dict)
        if not ret_dict:
            print("1111111111111")
            return redirect(homeView)
        ret_code = ret_dict.get("RetCode", None)
        if ret_code == "200":
            use_gk = ret_dict.get("GKUseGK", None)
            gk_addr = ret_dict.get("GKIPAddr", None)
            if use_gk is not None and gk_addr is not None:
                form = gkForm({"active": use_gk != "0", "ip": gk_addr, "e164": getmcue164()})
                return render(request, 'system_manage/GK_config.html', {'form': form})

        return render(request, 'system_manage/GK_config.html')
