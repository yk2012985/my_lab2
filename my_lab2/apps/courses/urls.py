from django.conf.urls import url
from .views import LessonAddView, LessonAddSubmitView
urlpatterns = [

    url(r'^lesson_add$', LessonAddView.as_view(), name='lesson_add'),

    url(r'^lesson/add_submit', LessonAddSubmitView.as_view(), name='lesson_add_submit'),


]























































