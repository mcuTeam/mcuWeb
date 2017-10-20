from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mcuWeb.celery import *
# Create your views here.

@login_required
def homeView(request):
	print("send task")
	testTask.apply_async()
	return render(request,'home.html')

def test(request):
	pass
	pass