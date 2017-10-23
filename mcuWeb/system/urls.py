from django.conf.urls import url
from system import views as system_view

urlpatterns = [
    url(r'^home/$', system_view.homeView),
    url(r'^$', system_view.homeView),


    url(r'^addmeet/$', system_view.addMeetView),
    url(r'^deletemeet/$', system_view.delMeetView),
]