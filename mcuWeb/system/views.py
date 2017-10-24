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

def analysisListMeetResult(retCode):
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
	meetInfo = re.split('\|',retDict['MeetPara'])
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

# --------------------------------------------------------------------------------------------------------------------------------------------

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
	if data is None:
		print("return None")
		return render(request,'home.html')
	ret = returnCode2Dict(data)
	if ret['RetCode'] != '200':
		print(type(ret['RetCode']))
		print(type('200'))
		print(ret['RetCode'] is '200')
		print("error0 occurs")
	result = setmeetgeneraparaTask.apply_async((meetName,))
	try:
		data = result.get(timeout=2)
		print("setmeetgeneraparaTask result:",data)
	except TimeoutError as e:
		print("timeout error: ",e)
		return render(request,'home.html')	
	ret.clear()
	if data is  None:
		print("return None")
	else:
		ret = returnCode2Dict(data)	
		if ret['RetCode'] != '200':
			print(ret['RetCode'])
			print("error1 occurs")
	return render(request,'home.html')

@login_required
def delMeetView(request):
	deletemeetTask.apply_async()
	return render(request,'home.html')


@login_required
def listMeetView(request):
	result = listmeetTask.apply_async()
	try:
		data = result.get(timeout=2)
		# print("addmeetTask result:",data)
		result = analysisListMeetResult(data)
		print(result)
	except TimeoutError as e:
		print("timeout error: ",e)
		return render(request,'home.html')
	return render(request,'home.html')

def test(request):
	pass
	pass