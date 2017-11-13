from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def creat_meetingView(request):
	return render(request,'meeting_manage/creat_meeting.html')

@login_required
def meetinglistView(request):
	return render(request,'meeting_manage/meetinglist.html')