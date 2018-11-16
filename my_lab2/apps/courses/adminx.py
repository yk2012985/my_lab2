import xadmin

from .models import Course,Lesson, LessonResource


class CourseAdmin(object):
    list_display = ('name', 'detail', 'add_time')
    search_fields= ('name')


class LessonAdmin(object):
    list_display = ('title', 'detail', 'add_time', 'course')
    list_filter = ['title',]#这句在后台管理系统中会添加过滤器框，按照列表中给定的字段对类进行过滤


class LessonResourceAdmin(object):
    list_display = ('name', 'lesson', 'add_time')
    list_filter = ['name',]#这句在后台管理系统中会添加过滤器框，按照列表中给定的字段对类进行过滤

# class LessonFileAdmin(object):
#     pass
#
#
# class CourseResourceAdmin(object):
#     pass


xadmin.site.register(Course,CourseAdmin)
xadmin.site.register(Lesson,LessonAdmin)
xadmin.site.register(LessonResource,LessonResourceAdmin)
# xadmin.site.register(CourseResource,CourseResourceAdmin)