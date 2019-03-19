# coding:utf-8
import configparser
from configobj import ConfigObj
import io
import os
import re
import shutil
import zipfile

import pythoncom
import wmi
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm, AdminPasswordChangeForm
from django.contrib.auth.models import User as sysUser
from django.contrib.auth.decorators import user_passes_test

# from fun.views import get_gk_status_task, set_gk_task
from system.forms import *
# from fun.views import *


# Create your views here.

def if_not_zby(user):
    print "if_not_zby:", user
    new_group, created = Group.objects.get_or_create(name="user")
    return new_group not in user.groups.all()


def returnCode2Dict(retCode):
    if type(retCode) is not str:
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
    if type(retCode) is not str:
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
    meetInfo = re.split("\|", retDict['MeetPara'])
    for item in meetInfo:
        # print(item)
        deep1 = re.split(r';', item)
        # print("deep1: ",deep1)
        for itemD1 in deep1:
            deep2 = re.split(r'=', itemD1, 1)
            # print(deep2)
            if deep2[0] in retDict and len(deep2) > 1:
                retDict[deep2[0]].append(deep2[1])
            elif len(deep2) > 1:
                retDict[deep2[0]] = []
                retDict[deep2[0]].append(deep2[1])
    return retDict


def checkSystem():
    if mcuAttributes.objects.count() < 1:
        tmp = mcuAttributes(alias="default", logLevel=0)
        tmp.save()


# --------------------------------------------------------------------------------------------------------------------------------------------

@login_required
def homeView(request):
    # heartBeat = checkNet.apply_async()
    # result=""
    # try:
    #     result = heartBeat.get(timeout=3)
    #     print(result)
    # except BaseException as e:
    #     print("catch heartbeat error",e)
    #     print(result)
    checkSystem()
    return render(request, 'home.html')


# @login_required
# def addMeetView(request):
#     print("adding meet by WuNL!")
#     current_time = datetime.datetime.now()
#     meetName = "%s" % current_time
#     meetRemark = meetName
#     result = addmeetTask.apply_async((meetName, meetRemark))
#     try:
#         data = result.get(timeout=3)
#         print("addmeetTask result:", data)
#     except TimeoutError as e:
#         print("timeout error: ", e)
#         return render(request, 'base.html')
#     if data is None:
#         print("return None")
#         return render(request, 'base.html')
#     ret = returnCode2Dict(data)
#     if ret['RetCode'] != '200':
#         print(type(ret['RetCode']))
#         print(type('200'))
#         print(ret['RetCode'] is '200')
#         print("error0 occurs")
#     result = setmeetgeneraparaTask.apply_async((meetName,))
#     try:
#         data = result.get(timeout=3)
#         print("setmeetgeneraparaTask result:", data)
#     except TimeoutError as e:
#         print("timeout error: ", e)
#         return render(request, 'base.html')
#     ret.clear()
#     if data is None:
#         print("return None")
#     else:
#         ret = returnCode2Dict(data)
#         if ret['RetCode'] != '200':
#             print(ret['RetCode'])
#             print("error1 occurs")
#     return render(request, 'base.html')
#
#
# @login_required
# def delMeetView(request):
#     # deletemeetTask.apply_async()
#     return render(request, 'base.html')
#
#
# @login_required
# def listMeetView(request):
#     result = listmeetTask.apply_async()
#     try:
#         data = result.get(timeout=3)
#         # print("addmeetTask result:",data)
#         result = analysisListMeetResult(data)
#         print(result)
#     except TimeoutError as e:
#         print("timeout error: ", e)
#         return render(request, 'base.html')
#     return render(request, 'base.html')


def test(request):
    pass
    pass


@login_required
def system_infoView(request):
    cf = configparser.ConfigParser()
    productname = ""
    maxactivecallnumber = ""
    MCUVersion = ''
    seris = ""
    remark = ""
    try:
        # os.chdir("C:\SVCMMCUAutoStart")
        cf.read("C:\SVCMMCUAutoStart\svcmmcu.ini")
        productname = cf.get("svcmmcu::main", "productname")
        maxactivecallnumber = cf.get("svcmmcu::main", "maxactivecallnumber")
        MCUVersion = cf.get("svcmmcu::main", "MCUVersion")
        remark = cf.get("svcmmcu::main", "remark")
        seris = cf.get("svcmmcu::main", "MCUVersion")
    except BaseException as e:
        print("system_infoView error occurs: ", e)
    return render(request, 'system_manage/system_info.html',
                  {'productname': productname, 'maxactivecallnumber': maxactivecallnumber, \
                   'MCUVersion': MCUVersion, 'remark': remark, 'seris': seris})


@login_required
def MCU_configView(request):
    if request.POST:
        curTime = request.POST['curTime']
        curDate = request.POST['curDate']
        print(curDate, curTime)
        os.system("date %s" % curDate)
        os.system("time %s" % curTime)
        if mcuAttributes.objects.count() < 1:
            tmp = mcuAttributes(alias="default", logLevel=0)
            tmp.save()
        mcuInstance = mcuAttributes.objects.get(pk=1)
        # print(request.POST)
        form = mcuAttributesForm(data=request.POST, instance=mcuInstance)
        # print(form)
        if form.is_valid():
            print("is valid")
            form.save()
        return render(request, 'system_manage/MCU_config.html', {'form': form})
    else:
        if mcuAttributes.objects.count() < 1:
            tmp = mcuAttributes(alias="default", logLevel=0)
            tmp.save()
        mcuInstance = mcuAttributes.objects.get(pk=1)
        form = mcuAttributesForm(instance=mcuInstance)
        return render(request, 'system_manage/MCU_config.html', {'form': form})




def getNetworkInfo():
    pythoncom.CoInitialize()
    nic_configs = wmi.WMI('').Win32_NetworkAdapterConfiguration(IPEnabled=True)
    if len(nic_configs) == 0:
        return None
    tmplist = []
    for interface in nic_configs:
        tmpdict = {}
        # Index
        tmpdict["Index"] = interface.Index
        # print(interface.Index)
        # IP
        tmpdict["IP"] = interface.IPAddress[0]
        # 描述
        tmpdict["Description"] = interface.Description
        # 掩码
        tmpdict["IPSubnet"] = interface.IPSubnet[0]
        # 网关
        if interface.DefaultIPGateway != None:
            tmpdict["DefaultIPGateway"] = interface.DefaultIPGateway[0]
        else:
            tmpdict["DefaultIPGateway"] = ""
        # DNS
        if interface.DNSServerSearchOrder != None:
            tmpdict["DNSServerSearchOrder"] = interface.DNSServerSearchOrder[0]
        else:
            tmpdict["DNSServerSearchOrder"] = ""
        # MAC
        tmpdict["MAC"] = interface.MacAddress
        tmplist.append(tmpdict)
    return tmplist


# 根据输入的参数配置网卡参数
# 输入：包含参数的字典
# 输出：True代表配置成功；失败则返回具体原因
def setNetworkInfo(paramDict):
    pythoncom.CoInitialize()
    c = wmi.WMI()
    tmplist = []
    colNicConfigs = c.Win32_NetworkAdapterConfiguration(IPEnabled=1)
    if len(colNicConfigs) < 1:
        return u"没有可用网卡"
    arrIPAddresses = [paramDict['IP']]
    arrSubnetMasks = [paramDict['IPSubnet']]
    arrDefaultGateways = [paramDict['DefaultIPGateway']]
    arrGatewayCostMetrics = [1]
    intReboot = 0
    for interface in colNicConfigs:
        if interface.Description == paramDict['Description'] and interface.Index == paramDict['Index']:
            print(paramDict)
            returnValue = interface.EnableStatic(IPAddress=arrIPAddresses, SubnetMask=arrSubnetMasks)
            if returnValue[0] == 0:
                print("  ")
            elif returnValue[0] == 1:
                intReboot += 1
            else:
                print(returnValue)
                return u"修改IP失败"
            returnValue = interface.SetGateways(DefaultIPGateway=arrDefaultGateways,
                                                GatewayCostMetric=arrGatewayCostMetrics)
            if returnValue[0] == 0 or returnValue[0] == 1:
                print("  ")
            elif returnValue[0] == 1:
                intReboot += 1
            else:
                return u"修改网关失败"
            if intReboot > 0:
                print("need reboot")
    return True


def setlocalip(localip):
    try:
        config = ConfigObj("C:\SVCMMCUAutoStart\svcmmcu.ini")
        config['svcmmcu::main']['Local IP'] = localip.encode("gb2312")
        config.write()
    except BaseException as e:
        print("setmcue164 error occurs: ", e)


@login_required
def port_configView(request):
    if request.POST:
        adapterInstance = networkAdapterForm(request.POST)
        if adapterInstance.is_valid():
            print("is valid")
            localip = adapterInstance.cleaned_data["IP"]
            index = adapterInstance.cleaned_data["Index"]
            print(index, localip)
            setlocalip(localip)
            os.system('taskkill /f /im "SVCMMCU.exe"')

            ret = setNetworkInfo(adapterInstance.cleaned_data)
            print(ret)
            return HttpResponseRedirect('/port_config/')
        else:
            print("is not valid")
            return HttpResponseRedirect('/port_config/')
    else:
        ret = getNetworkInfo()
        if ret is None:
            print("no network!")
        if ret is None:
            networkAdapter1 = None
            networkAdapter2 = None
        elif len(ret) == 2:
            data1 = ret[0]
            data2 = ret[1]
            networkAdapter1 = networkAdapterForm(data1)
            networkAdapter2 = networkAdapterForm(data2)
        elif len(ret) == 1:
            data1 = ret[0]
            networkAdapter1 = networkAdapterForm(data1)
            networkAdapter2 = None
        else:
            data1 = ret[0]
            data2 = ret[1]
            networkAdapter1 = networkAdapterForm(data1)
            networkAdapter2 = networkAdapterForm(data2)
        return render(request, 'system_manage/port_config.html',
                      {'networkAdapter1': networkAdapter1, 'networkAdapter2': networkAdapter2})

    # if gkAttributes.objects.count() < 1:
    #     tmp = gkAttributes(ip="0.0.0.0", active=False)
    #     tmp.save()
    # gk = gkAttributes.objects.get(pk=1)
    # if request.POST:
    #     print("post!!")
    #     gkFormInstance = gkForm(data=request.POST, instance=gk)
    #     if gkFormInstance.is_valid():
    #         print("gkForm valid")
    #         gkFormInstance.save(commit=True)
    #         return HttpResponseRedirect('/GK_config/')
    #     else:
    #         return render(request, 'system_manage/GK_config.html', {'form': gkFormInstance})
    #     return render(request, 'system_manage/GK_config.html')
    # else:
    #     form = gkForm(instance=gk)
    #     return render(request, 'system_manage/GK_config.html', {'form': form})


def handle_upload_file(f):
    updateDirectory = "C:/SVCMMCUAutoStart/"
    if f.name != "update.zip":
        return u"请输入update.zip升级包"
    else:
        if zipfile.is_zipfile(f):
            pass
            try:
                zp = zipfile.ZipFile(f, 'r')
                # zp.extractall(updateDirectory)
                for filename in zp.namelist():
                    os.system('taskkill /f /im "SVCMMCU.exe"')
                    print(filename)
                    strname = filename.decode('gb2312')
                    if '/' in strname:
                        print(os.path.dirname(updateDirectory + strname))
                        if not os.path.exists(os.path.dirname(updateDirectory + strname)):
                            os.makedirs(os.path.dirname(updateDirectory + strname))
                        f_handle = open(updateDirectory + strname, "w+b")
                        f_handle.write(zp.read(filename))
                        f_handle.close()
                    else:
                        f_handle = open(updateDirectory + strname, "w+b")
                        f_handle.write(zp.read(filename))
                        f_handle.close()
                zp.close()
                return True
            except BaseException as e:
                print(e)
                return e
        else:
            return u"请输入update.zip升级包"

        return True


@login_required
def sw_manageView(request):
    if request.POST:
        form = uploadFileForm(request.POST, request.FILES)
        print(form)
        if form.is_valid():
            print("file form is valid!")
            handleFileResult = handle_upload_file(request.FILES['file'])
            if handleFileResult != True:
                return render(request, 'system_manage/sw_manage.html',
                              {'form': form, 'msgType': "error", 'msg': handleFileResult})
            form = uploadFileForm()
            return render(request, 'system_manage/sw_manage.html', {'form': form, 'msgType': "success", 'msg': u"上传成功"})
        else:
            print(form)
            return render(request, 'system_manage/sw_manage.html', {'form': form, 'msgType': "error", 'msg': u"填写错误！"})
    form = uploadFileForm()
    return render(request, 'system_manage/sw_manage.html', {'form': form})


def handle_config_file(f):
    print(f)
    print(type(f))
    updateDirectory = "C:/SVCMMCUAutoStart/"
    if f.name != "svcmmcu.ini":
        return u"请输入配置文件：svcmmcu.ini"
    else:
        try:
            os.system('taskkill /f /im "SVCMMCU.exe"')
            f_handle = open(updateDirectory + f.name, "w+b")
            for chunk in f.chunks():
                f_handle.write(chunk)
            f_handle.close()
        except BaseException as e:
            return e
    return True


@login_required
def configfileView(request):
    if request.POST:
        form = uploadConfigFileForm(request.POST, request.FILES)
        if form.is_valid():
            print("configfile form is valid!")
            handleFileResult = handle_config_file(request.FILES['file'])
            if handleFileResult != True:
                return render(request, 'system_manage/configfile.html',
                              {'form': form, 'msgType': "error", 'msg': handleFileResult})
            form = uploadConfigFileForm()
            return render(request, 'system_manage/configfile.html',
                          {'form': form, 'msgType': "success", 'msg': u"上传成功"})
        else:
            print("configfile form is not valid!", form)
            return render(request, 'system_manage/configfile.html', {'form': form, 'msgType': "error", 'msg': u"填写错误！"})
    form = uploadConfigFileForm()
    return render(request, 'system_manage/configfile.html', {'form': form})


configfileDir = "C:/SVCMMCUAutoStart/"

@login_required
def downloadconfigfileView(request):
    filename = configfileDir + 'svcmmcu.ini'
    # print fileNames
    zip_subdir = str("configfile")  # name of the zip file to be
    zip_filename = "%s.zip" % zip_subdir
    s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w")

    fdir, fname = os.path.split(filename)
    zip_path = os.path.join(zip_subdir, fname)
    zf.write(filename, zip_path)
    zf.close()
    resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
    return resp


logDir = "C:/SVCMMCUAutoStart/LOGFILE/"


def getFileNames():
    fileSet = set()
    for dir_, _, files in os.walk(logDir):
        for fileName in files:
            # relDir = os.path.relpath(dir_, rootDir)
            relFile = os.path.join(fileName)
            fileSet.add(relFile)
    return list(fileSet)


@login_required
def downloadLogView(request):
    fileNames = []
    files = getFileNames()
    for names in files:
        fileNames.append(logDir + names)
    # print fileNames
    zip_subdir = str(datetime.date.today())  # name of the zip file to be
    zip_filename = "%s.zip" % zip_subdir
    s = io.BytesIO()
    zf = zipfile.ZipFile(s, "w")
    for fpath in fileNames:
        fdir, fname = os.path.split(fpath)
        zip_path = os.path.join(zip_subdir, fname)
        zf.write(fpath, zip_path)
    zf.close()
    resp = HttpResponse(s.getvalue(), content_type="application/x-zip-compressed")
    resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
    return resp


@login_required
def clearLogView(request):
    try:
        shutil.rmtree("C:/SVCMMCUAutoStart/LOGFILE")
    except Exception as e:
        return HttpResponse(u"部分文件占用，删除失败")
    return HttpResponse(u"操作成功")


@login_required
def rebootView(request):
    os.system("shutdown -r -t 5")
    return HttpResponse(u"操作成功")


@login_required
def shutdownView(request):
    os.system("shutdown -s -t 5")
    return HttpResponse(u"操作成功")


@login_required
def restartMCUView(request):
    ret1 = os.system('taskkill /f /im "SVCMMCU.exe"')
    if ret1 == 0:
        return HttpResponse(u"操作成功")
    return HttpResponse(u"关闭进程失败，可能mcu未启动")


@login_required
@user_passes_test(if_not_zby,login_url="/home/" )
def useraccountsView(request):
    new_group, created = Group.objects.get_or_create(name="user")

    zbyList = new_group.user_set.all()
    return render(request, 'system_manage/zbys.html', {"zbyList": zbyList})


@login_required
@user_passes_test(if_not_zby,login_url="/home/" )
def adduseraccountsView(request):
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print "user valid!"

            user = form.save(commit=False)
            user.is_superuser = True
            user.is_staff = True
            user.save()

            new_group, created = Group.objects.get_or_create(name="user")
            new_group.user_set.add(user)
            return HttpResponseRedirect("/useraccounts/")
        else:
            return render(request, 'system_manage/addZbyAccount.html', {"form": form})
    form = UserCreationForm()
    return render(request, 'system_manage/addZbyAccount.html', {"form": form})


@login_required
@user_passes_test(if_not_zby,login_url="/home/" )
def deleteuseraccountsView(request, acpk):
    instance = get_object_or_404(sysUser, pk=int(acpk))
    instance.delete()
    return HttpResponseRedirect("/useraccounts/")
