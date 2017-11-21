from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect,HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse,HttpResponseServerError

from fun.forms import *
from system.models import *
from system.views import *

from mcuWeb.celery import *
# Create your views here.

def syncMeetingListAndDB(result):
	meeting.objects.all().delete()
	meetingNumber = result['MeetCount']
	for index in range(0,int(meetingNumber)):
		# filtered = meeting.objects.filter(name=result['MeetName'][index],meetcode=result['MeetAlias'][index])
		# if not filtered.exists():
		meetingInstance = meeting(name=result['MeetName'][index],meetcode=result['MeetAlias'][index],remark=result['MeetRemark'][index])
		meetingInstance.save()
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
			try:
				data = addmeetTask.apply_async((meetName,MeetAlias,meetRemark)).get(timeout=3)
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
			result = setmeetgeneraparaTask.apply_async((meetName,))
			try:
				data = result.get(timeout=3)
				print("setmeetgeneraparaTask result:",data)
			except BaseException as e:
				print("timeout error: ",e)
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
				return redirect(meetinglistView)
				# return render(request,'fun/meetinglist.html',{'meetinglist':meetinglist,'msgType':msgType,'msg':msg})
		else:
			return render(request,'fun/creat_meeting.html',{'meetform':meetform,'msgType':"error",'msg':"填写错误，请重新提交"})
	else:
		meetform = meetingForm()
		return render(request,'fun/creat_meeting.html',{'meetform':meetform,'msgType':"info",'msg':"请添加会议"})


@login_required
def meetinglistView(request,msgType='',msg=''):
	try:
		data = listmeetTask.apply_async().get(timeout=3)
		print("1")
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

@login_required
def heartBeatAjaxView(request):
	if request.is_ajax():
		print("recv ajax request")
		return HttpResponse("success")
