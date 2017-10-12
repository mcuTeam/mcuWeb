from django.conf.urls import url
from system import views as system_view

urlpatterns = [
    url(r'^home/', system_view.homeView),
]