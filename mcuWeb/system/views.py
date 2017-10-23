from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mcuWeb.celery import *
import datetime
# Create your views here.

@login_required
def homeView(request):
	testTask.apply_async()
	return render(request,'home.html')

@login_required
def addMeetView(request):
	print("adding meet by WuNL!")
	current_time = datetime.datetime.now()
	meetName = "%s" % current_time
	meetRemark = meetName
	addmeetTask.apply_async(meetName,meetRemark)
	return render(request,'home.html')

@login_required
def delMeetView(request):
	deletemeetTask.apply_async()
	return render(request,'home.html')


def test(request):
	pass
	pass