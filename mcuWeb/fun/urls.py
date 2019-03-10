from django.conf.urls import url

from fun import views as fun_view

urlpatterns = [
    url(r'^creat_meeting/$', fun_view.creat_meetingView),
    url(r'^delete_meeting/(?P<meetpk>\d+)/$', fun_view.delete_meetingView),
    url(r'^meetinglist/$', fun_view.meetinglistView),
    url(r'^terminallistP/$', fun_view.terminallistViewP),

    url(r'^terminallist/$', fun_view.terminallistView, {'msg': ""}, name='terminallist'),
    url(r'^addterminal/$', fun_view.addterminalView),
    url(r'^deleteterminal/(?P<terminalpk>\d+)/$', fun_view.deleteterminalView),

    url(r'^templatelist/$', fun_view.templatelistView),
    url(r'^addtemplate/$', fun_view.addtemplateView),
    url(r'^deletetemplate/(?P<templatepk>\d+)/$', fun_view.deletetemplateView),

    url(r'^meetDetails/(?P<meetpk>\d+)/$', fun_view.meetDetailsView),

    url(r'^csmeetDetails/(?P<meetname>\w+)/$', fun_view.csmeetDetailsView),
    url(r'^getcsmeetinfo/(?P<meetname>\w+)/$', fun_view.getcsmeetinfoAjaxView),

    url(r'^mcuHeartBeat/$', fun_view.heartBeatAjaxView),
    url(r'^callmember/(?P<meetpk>\d+)/(?P<pk>\d+)/$', fun_view.callmemberAjaxView),
    url(r'^hangup/(?P<meetpk>\d+)/(?P<pk>\d+)/$', fun_view.hungupAjaxView),
    url(r'^silencemember/(?P<meetpk>\d+)/(?P<pk>\d+)/(?P<mode>\d+)/$', fun_view.audioblockAjaxView),
    url(r'^shutup/(?P<meetpk>\d+)/(?P<pk>\d+)/(?P<mode>\d+)/$', fun_view.silencememberAjaxView),
    url(r'^double/(?P<meetpk>\d+)/(?P<pk>\d+)/(?P<mode>\d+)/$', fun_view.setsecondvideosrcAjaxView),

    url(r'^see/(?P<meetpk>\d+)/(?P<pk>\d+)/(?P<mode>\d+)/$', fun_view.seeAjaxView),
    url(r'^broadcast/(?P<meetpk>\d+)/(?P<pk>\d+)/(?P<mode>\d+)/$', fun_view.broadcastAjaxView),

    url(r'^getmeetinfo/(?P<meetpk>\d+)/$', fun_view.getmeetinfoAjaxView),
    url(r'^hungupall/(?P<meetpk>\d+)/$', fun_view.hungupallAjaxView),
    url(r'^callall/(?P<meetpk>\d+)/$', fun_view.callallAjaxView),

    url(r'^model/(?P<meetpk>\d+)/(?P<mode>\d+)/$', fun_view.setoperationmodeAjaxView),
]
