import xadmin
from .models import Laboratory, Desk, Device


class LaboratoryAdmin(object):
    list_display = ('name', 'locate', 'detail', 'add_time')
    search_fields = ('name')


class DeskAdmin(object):
    list_display = ('number', 'lab', 'row', 'column')
    search_fields = ('number', 'lab', 'row','column')
    list_filter = ['number', 'row', 'column']

class DeviceAdmin(object):
    pass


xadmin.site.register(Laboratory, LaboratoryAdmin)
xadmin.site.register(Desk, DeskAdmin)
xadmin.site.register(Device, DeviceAdmin)
