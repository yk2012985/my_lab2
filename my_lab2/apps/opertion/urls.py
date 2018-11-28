from django.conf.urls import url
from .views import LessonPublicView, LessonPublicSubmitView, LessonPublicInfoView,LessonPublicDeleteView\
    , LessonPublicEditView
urlpatterns = [

    url(r'^lesson/public', LessonPublicView.as_view(), name='lesson_public'),

    url(r'^add_lesson_public/$', LessonPublicSubmitView.as_view(), name='lesson_public_submit'),



    url(r'^lesson/info/(?P<lesson_id>\d+)$', LessonPublicInfoView.as_view(), name='lesson_info'),

    url(r'^lesson/edit/(?P<lesson_id>\d+)$', LessonPublicEditView.as_view(), name='lesson_edit'),

    url(r'^lesson/delete/(?P<lesson_id>\d+)$', LessonPublicDeleteView.as_view(), name='lesson_delete'),

    # url(r'^lesson/edit/(?P<lesson_id>\d+)$', LessonPublicEditView.as_view(), name='lesson_edit'),
    #
    # url(r'^lesson_add$', LessonAddView.as_view(), name='lesson_add'),
 ]