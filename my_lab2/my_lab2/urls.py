"""my_lab2 URL Configuration

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
from django.conf.urls import url, include
from django.views.static import serve
from my_lab2.settings import MEDIA_ROOT
from django.contrib import admin
import xadmin
from users.views import LoginView, IndexView, logout, TeacherIndexView, StudentIndexView
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^login/', LoginView.as_view(), name='user_login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^$', IndexView.as_view(), name='index'),

    url(r'^course/', include('courses.urls', namespace='course')),

    url(r'^operation/', include('opertion.urls', namespace='operation')),


    url(r'^teacher_index/', TeacherIndexView.as_view(), name='teacher_index'),
    url(r'^student_index/', StudentIndexView.as_view(), name='student_index'),

    url(r'^lab/', include('measure.urls', namespace='lab')),

    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
]
