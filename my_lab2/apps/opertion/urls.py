from django.conf.urls import url
from .views import LessonPublicView, LessonPublicSubmitView, LessonPublicInfoView, TeacherLessonPublicInfoView,LessonPublicDeleteView\
    , LabLessonsView, LabDatePublicView, LessonSubscribeView, LessonSubscribeDeleteView, ReportResultSaveView\
    ,StudentLessonInfoView,LessonPublicDoneView, LessonPublicUndoneView, LessonPublicPersonalDoneView, LessonPublicPersonalUndoneView\
    ,LessonSubscribePersonalDoneView,LessonSubscribePersonalUndoneView, LabLessondoneView, LabLessonUndoneView, LabDeskSheetView\
    ,LabDeskCheckView
urlpatterns = [

    # 返回所有已完成实验课
    url(r'^lesson/public/done$', LessonPublicDoneView.as_view(), name='lesson_public_done'),

    # 返回所有未完成实验课
    url(r'^lesson/public/undone$', LessonPublicUndoneView.as_view(),name='lesson_public_undone'),

    # 返回教师个人所有已完成实验课
    url(r'^lesson/public/personal/done$', LessonPublicPersonalDoneView.as_view(), name='lesson_public_personal_done'),

    # 返回教师个人所有未完成实验课
    url(r'^lesson/public/personal/undone$', LessonPublicPersonalUndoneView.as_view(), name='lesson_public_personal_undone'),

    # 返回学生个人所有已完成实验课
    url(r'^lesson/subscribe/personal/done$', LessonSubscribePersonalDoneView.as_view(), name='lesson_subscribe_personal_done'),

    # 返回学生个人所有未完成实验课
    url(r'^lesson/subscribe/personal/undone$', LessonSubscribePersonalUndoneView.as_view(), name='lesson_subscribe_personal_undone'),



    url(r'^lesson/public', LessonPublicView.as_view(), name='lesson_public'),

    # 返回实验室所有完成实验情况
    url(r'^lab/lesson/done$', LabLessondoneView.as_view(), name='lab_lesson_done'),

    # 返回实验室所有未完成实验情况
    url(r'^lab/lesson/undone$', LabLessonUndoneView.as_view(), name='lab_lesson_undone'),

    url(r'^add_lesson_public/$', LessonPublicSubmitView.as_view(), name='lesson_public_submit'),


    # 已发布实验信息详情
    url(r'^lesson/info/(?P<lesson_id>\d+)$', LessonPublicInfoView.as_view(), name='lesson_info'),


    # 教师实验信息详情
    url(r'^lesson/teacher/info/(?P<lesson_id>\d+)$', TeacherLessonPublicInfoView.as_view(), name='teacher_lesson_info'),

    # 学生实验信息详情
    url(r'^lesson/student/info/(?P<lesson_id>\d+)$', StudentLessonInfoView.as_view(), name='student_lesson_info'),

    #url(r'^lesson/edit/(?P<lesson_id>\d+)$', LessonPublicEditView.as_view(), name='lesson_edit'),

    url(r'^lesson/delete/(?P<lesson_id>\d+)$', LessonPublicDeleteView.as_view(), name='lesson_delete'),

    # 异步询问实验室实验信息
    url(r'^lab_lessons', LabLessonsView.as_view(), name='lab_lessons'),

    #异步询问某实验室某个日期的实验发布情况
    #url(r'^input_test/(?P<lab_id>\d+)$', InputTestView.as_view(), name="input_test"),

    url(r'^lab_date_public/(?P<lab_id>\d+)$', LabDatePublicView.as_view(), name='lab_date_public'),

    # 查看实验室有无满员情况
    url(r'^lab_desk_check/$', LabDeskCheckView.as_view(), name='lab_desk_check'),

    # 展示实验台页面
    url(r'^lab_desk_sheet/(?P<lesson_id>\d+)$', LabDeskSheetView.as_view(), name='lab_desk_sheet'),

    # 学生预约实验
    url(r'^lesson_subscribe/(?P<lesson_id>\d+)/(?P<desk_id>\d+)$', LessonSubscribeView.as_view(), name='lesson_subscribe'),

    # 学生预约实验删除
    url(r'^lesson_subscribe_delete/(?P<lesson_subscribe_id>\d+)$', LessonSubscribeDeleteView.as_view(), name='lesson_subscribe_delete'),


    # 实验报告批改结果保存
    url(r'^report_result_save$', ReportResultSaveView.as_view(), name='report_result_save'),



    # url(r'^lesson/edit/(?P<lesson_id>\d+)$', LessonPublicEditView.as_view(), name='lesson_edit'),
    #
    # url(r'^lesson_add$', LessonAddView.as_view(), name='lesson_add'),
 ]