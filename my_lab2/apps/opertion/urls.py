from django.conf.urls import url
from .views import LessonPublicView, LessonPublicSubmitView, LessonPublicInfoView,LessonPublicDeleteView\
    , LabLessonsView, LabDatePublicView, LessonSubscribeView, LessonSubscribeDeleteView, ReportResultSaveView\
    ,StudentLessonInfoView
urlpatterns = [

    url(r'^lesson/public', LessonPublicView.as_view(), name='lesson_public'),

    url(r'^add_lesson_public/$', LessonPublicSubmitView.as_view(), name='lesson_public_submit'),


    # 教师实验信息详情
    url(r'^lesson/info/(?P<lesson_id>\d+)$', LessonPublicInfoView.as_view(), name='lesson_info'),

    # 学生实验信息详情
    url(r'^lesson/student/info/(?P<lesson_id>\d+)$', StudentLessonInfoView.as_view(), name='student_lesson_info'),

    #url(r'^lesson/edit/(?P<lesson_id>\d+)$', LessonPublicEditView.as_view(), name='lesson_edit'),

    url(r'^lesson/delete/(?P<lesson_id>\d+)$', LessonPublicDeleteView.as_view(), name='lesson_delete'),

    # 异步询问实验室实验信息
    url(r'^lab_lessons', LabLessonsView.as_view(), name='lab_lessons'),

    #异步询问某实验室某个日期的实验发布情况
    #url(r'^input_test/(?P<lab_id>\d+)$', InputTestView.as_view(), name="input_test"),

    url(r'^lab_date_public/(?P<lab_id>\d+)$', LabDatePublicView.as_view(), name='lab_date_public'),

    # 学生预约实验
    url(r'^lesson_subscribe$', LessonSubscribeView.as_view(), name='lesson_subscribe'),

    # 学生预约实验删除
    url(r'^lesson_subscribe_delete/(?P<lesson_subscribe_id>\d+)$', LessonSubscribeDeleteView.as_view(), name='lesson_subscribe_delete'),


    # 实验报告批改结果保存
    url(r'^report_result_save$', ReportResultSaveView.as_view(), name='report_result_save'),



    # url(r'^lesson/edit/(?P<lesson_id>\d+)$', LessonPublicEditView.as_view(), name='lesson_edit'),
    #
    # url(r'^lesson_add$', LessonAddView.as_view(), name='lesson_add'),
 ]