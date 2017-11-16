from django.conf.urls import url
from system import views as system_view
from fun import views as fun_view

urlpatterns = [
	url(r'^creat_meeting/$', fun_view.creat_meetingView),
	url(r'^meetinglist/$', fun_view.meetinglistView),

	url(r'^terminallist/$', fun_view.terminallistView),
	url(r'^addterminal/$', fun_view.addterminalView),
]