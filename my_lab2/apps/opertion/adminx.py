import xadmin
from .models import LessonPublic, LessonSubscribe, LessonReport


class LessonPublicAdmin(object):
    list_display = ['teacher', 'lesson', 'lab', 'start_time', 'stop_time']
    search_fields = ['teacher', 'lesson', 'lab','add_time']
    list_filter = ['teacher', 'lesson', 'lab']


class LessonSubscribeAdmin(object):
    list_display = ['student', 'lesson']
    search_fields = ['student', 'lesson']
    list_filter = ['student', 'lesson']


class LessonReportAdmin(object):
    list_display = ['name', 'lesson', 'add_time']
    search_fields = ['name', 'lesson']
    list_filter = ['name', 'lesson']
    #pass


xadmin.site.register(LessonPublic, LessonPublicAdmin)
xadmin.site.register(LessonSubscribe, LessonSubscribeAdmin)
xadmin.site.register(LessonReport, LessonReportAdmin)
