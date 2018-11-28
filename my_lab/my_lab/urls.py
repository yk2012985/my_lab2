"""my_lab URL Configuration

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
from django.contrib import admin
import xadmin
from users.views import LoginView, index, logout
from instructor.views import teacher_index, student_index
from report.views import ReportView
from my_lab.settings import MEDIA_ROOT
from django.views.static import serve
urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^login/', LoginView.as_view(), name='login'),
    url(r'^logout/', logout, name='logout'),
    url(r'^teacher_index/', teacher_index, name='teacher_index'),
    url(r'^student_index/', student_index, name='student_index'),

    # url(r'^course/', include('courses.urls', namespace='course')),
    # url(r'^lab/', include('measure.urls', namespace='lab')),
    url(r'^report/', ReportView.as_view(), name='report'),

    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT})


]
 