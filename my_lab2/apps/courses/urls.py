from django.conf.urls import url
from .views import LessonAddView, LessonAddSubmitView, InputTestView
urlpatterns = [

    url(r'^lesson_add$', LessonAddView.as_view(), name='lesson_add'),

    url(r'^lesson/add_submit', LessonAddSubmitView.as_view(), name='lesson_add_submit'),

    url(r'^input_test/(?P<lab_id>\d+)$', InputTestView.as_view(), name="input_test"),
]























































