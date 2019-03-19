from django.conf.urls import url

from fun import views as fun_view
from system import views as system_view

urlpatterns = [
    url(r'^home/$', system_view.homeView),
    url(r'^$', system_view.homeView),
    url(r'^system_info/$', system_view.system_infoView),



    url(r'^MCU_config/$', system_view.MCU_configView),
    url(r'^port_config/$', system_view.port_configView),
    url(r'^GK_config/$', fun_view.GK_configView),
    url(r'^sw_manage/$', system_view.sw_manageView),
    url(r'^configfile/$', system_view.configfileView),
    url(r'^downloadconfigfile/$', system_view.downloadconfigfileView),

    url(r'^down_log/$', system_view.downloadLogView),

    # url(r'^addmeet/$', system_view.addMeetView),
    # url(r'^deletemeet/$', system_view.delMeetView),
    # url(r'^listmeet/$', system_view.listMeetView),

    url(r'^clear/$', system_view.clearLogView),
    url(r'^restart/$', system_view.restartMCUView),
    url(r'^shutdown/$', system_view.shutdownView),

    url(r'^useraccounts/$', system_view.useraccountsView),
    url(r'^adduseraccounts/$', system_view.adduseraccountsView),
    url(r'^deleteuseraccounts/(?P<acpk>\d+)/$', system_view.deleteuseraccountsView),
]
