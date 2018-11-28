from django.conf.urls import url
from .views import labs_view, lab_info, lab_edit, lab_edit_action, lab_delete
    # device_info, device_edit_page,device_edit_action
urlpatterns = [
    url(r'^labs/', labs_view, name='labs'),
    url(r'^lab_info/(?P<lab_id>[0-9]+)/', lab_info, name='lab_info'),
    url(r'^lab_edit_page/(?P<lab_id>[0-9]+)/', lab_edit, name='lab_edit_page'),
    url(r'^lab_edit_action', lab_edit_action, name='lab_edit_action'),
    url(r'^lab_delete/(?P<lab_id>[0-9]+)/', lab_delete,name='lab_delete'),

    # url(r'^device_info/(?P<d_id>[0-9]+)/', device_info, name='device_info'),
    # url(r'^device_edit_page/(?P<d_id>[0-9]+)/(?P<lab_id>[0-9]+)/', device_edit_page, name='device_edit_page'),
    # url(r'^device_edit_action', device_edit_action, name='device_edit_action'),
]
