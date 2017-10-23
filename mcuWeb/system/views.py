from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mcuWeb.celery import *
import datetime
import re
# Create your views here.

def returnCode2Dict(retCode):
	if type(retCode) is not str:
		return False
	s = re.sub(r'\r\n\r\n','',retCode)
	a = s.split('\r\n')
	retDict = {}
	for item in a:
	    res = re.split(r':',item,1)
	    print(res)
	    if len(res)<2:
	        retDict['RetName'] = res[0]
	    else:
	        retDict[res[0]] = res[1]
	return retDict

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
	result = addmeetTask.apply_async((meetName,meetRemark))
	try:
		data = result.get(timeout=2)
		print("addmeetTask result:",data)
	except TimeoutError as e:
		print("timeout error: ",e)
		return render(request,'home.html')
	ret = returnCode2Dict(data)
	if ret['RetCode'] is not '200':
		print("error occurs")
	result = setmeetgeneraparaTask.apply_async((meetName,))
	try:
		data = result.get(timeout=2)
		print("setmeetgeneraparaTask result:",data)
	except TimeoutError as e:
		print("timeout error: ",e)
		return render(request,'home.html')	
	print(ret)
	if ret['RetCode'] is not '200':
		print("error occurs")
	return render(request,'home.html')

@login_required
def delMeetView(request):
	deletemeetTask.apply_async()
	return render(request,'home.html')


def test(request):
	pass
	pass