from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def homeView(request):
	return render(request,'home.html')

def test(request):
	pass
	pass