import xadmin
from .models import Template
class TemplateAdmin(object):
    pass



xadmin.site.register(Template,TemplateAdmin)