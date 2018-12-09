from django.conf.urls import url
from .views import LessonAddView, LessonAddSubmitView, InputTestView, LessonPublicAllView
urlpatterns = [
    # 返回所有已发布的实验课
    url(r'^lesson/public/all$', LessonPublicAllView.as_view(), name='lesson_public_all'),

    #返回教师









    url(r'^lesson_add$', LessonAddView.as_view(), name='lesson_add'),

    url(r'^lesson/add_submit', LessonAddSubmitView.as_view(), name='lesson_add_submit'),

    url(r'^input_test/(?P<lab_id>\d+)$', InputTestView.as_view(), name="input_test"),
]























































