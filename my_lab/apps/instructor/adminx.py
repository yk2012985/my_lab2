import xadmin

from .models import Class
class ClassAdmin(object):
    pass


xadmin.site.register(Class,ClassAdmin)
