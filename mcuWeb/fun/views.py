from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from fun.forms import *
from system.models import *
# Create your views here.

@login_required
def creat_meetingView(request):
	return render(request,'meeting_manage/creat_meeting.html')

@login_required
def meetinglistView(request):
	return render(request,'meeting_manage/meetinglist.html')

@login_required
def terminallistView(request):
	terminalList = terminal.objects.all()
	return render(request,'fun/terminallist.html',{'terminallist':terminalList,'msgType':'info','msg':"hello!!!!"})

@login_required
def addterminalView(request):
	if request.POST:
		terminalform = terminalForm(request.POST)
		if terminalform.is_valid():
			terminalform.save(commit=True)
			terminalList = terminal.objects.all()
			return render(request,'fun/terminallist.html',{'terminallist':terminalList,'msgType':'success','msg':"add success!!!!"})
		else:
			return render(request,'fun/addterminal.html',{'terminalform':terminalform,'msgType':'error','msg':"fail to add"})	
	else:
		terminalform = terminalForm()
		return render(request,'fun/addterminal.html',{'terminalform':terminalform,'msgType':'info','msg':"please add"})