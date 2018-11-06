"""public URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from account import views as a_view

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/',a_view.login),
    path('weixin/login/',a_view.weixin_login),
    path('worker/',a_view.worker),
    path('employer/',a_view.employer),

    path('', w_v.index),
    path('insert/', w_v.insert),
    path('query/', w_v.query),
    path('get/<str:object_id>/', w_v.get),
]