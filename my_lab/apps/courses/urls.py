from django.conf.urls import url
from .views import CoursesList, course_information, course_edit_page, course_edit_action, course_delete,\
    upload_file_page, upload_file_action, lesson_info, lesson_edit_page, lesson_edit_action, lesson_delete,\
    course_file_context,course_file_download
urlpatterns = [
    # url(r'^list/', course_view, name='course_list'),
    url(r'^list/', CoursesList.as_view(), name='course_list'),

    url(r'^info/(?P<course_id>[0-9]+)/', course_information, name='course_info'),
    url(r'^course_edit_page/(?P<course_id>[0-9]+)/', course_edit_page, name='course_edit_page'),
    url(r'^course_edit_action/', course_edit_action, name='course_edit_action'),
    url(r'^delete/(?P<course_id>[0-9]+)/', course_delete, name='course_delete'),
    url(r'^file_context/(?P<file_id>[0-9]+)/', course_file_context, name='course_file_context'),
    url(r'^file_download/(?P<file_id>[0-9]+)/', course_file_download, name='course_file_download'),

    url(r'^lesson_info/(?P<lesson_id>[0-9]+)/', lesson_info, name='lesson_info'),
    url(r'^lesson_edit_page/(?P<course_id>[0-9]+)/(?P<lesson_id>[0-9]+)/', lesson_edit_page, name='lesson_edit_page'),
    url(r'^lesson_edit_action/', lesson_edit_action, name='lesson_edit_action'),
    url(r'^lesson_delete/(?P<course_id>[0-9]+)/(?P<lesson_id>[0-9]+)/', lesson_delete, name='lesson_delete'),

    url(r'^upload_file_page/(?P<course_id>[0-9]+)/', upload_file_page, name='upload_file_page'),
    url(r'^upload_file_action/', upload_file_action, name='upload_file_action'),
]