"""mcuWeb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import userena.views as userView
from django.conf.urls import url, include
from django.contrib import admin

from system.forms import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^accounts/signin/$', userView.signin, {'auth_form': SigninFormExtra}, name="userena_signin"),

    url(r'^accounts/', include('userena.urls')),

    url(r'', include('system.urls')),
    url(r'', include('fun.urls')),
    # url(r'^accounts/',include('accounts.urls')),
]
