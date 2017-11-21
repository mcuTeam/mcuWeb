from django.conf.urls import url
from system import views as system_view
from fun import views as fun_view

urlpatterns = [
	url(r'^creat_meeting/$', fun_view.creat_meetingView),
	url(r'^meetinglist/$', fun_view.meetinglistView),
	url(r'^terminallistP/$', fun_view.terminallistViewP),

	url(r'^terminallist/$', fun_view.terminallistView,{'msg':""},name='terminallist'),
	url(r'^addterminal/$', fun_view.addterminalView),

	url(r'^templatelist/$', fun_view.templatelistView),
	url(r'^addtemplate/$', fun_view.addtemplateView),

	url(r'^mcuHeartBeat/$', fun_view.heartBeatAjaxView),
]
