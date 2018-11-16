from django.conf.urls import url
from .views import TeacherIndexView, LessonPublicView, LessonPublicSubmitView
urlpatterns = [
    url(r'^teacher/index', TeacherIndexView.as_view(), name='teacher_index'),
    url(r'^lesson/public', LessonPublicView.as_view(), name='lesson_public'),
    url(r'^add_lesson_public/', LessonPublicSubmitView.as_view(), name='lesson_public_submit'),

]
