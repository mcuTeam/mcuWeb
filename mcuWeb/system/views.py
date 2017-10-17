from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from mcuWeb.celery import *
# Create your views here.

@login_required
def homeView(request):
	testTask.delay()
	return render(request,'home.html')

def test(request):
	pass
	pass