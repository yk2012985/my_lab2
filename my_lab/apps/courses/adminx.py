import xadmin

from .models import Course,Lesson,LessonFile,CourseResource


class CourseAdmin(object):
    list_display = ('name','desc','add_time')
    search_fields=('name')


class LessonAdmin(object):
    list_display = ('name','detail','add_time')
    list_filter = ['course__name',]#这句在后台管理系统中会添加过滤器框，按照列表中给定的字段对类进行过滤


class LessonFileAdmin(object):
    pass


class CourseResourceAdmin(object):
    pass


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(LessonFile,LessonFileAdmin)
xadmin.site.register(CourseResource,CourseResourceAdmin)