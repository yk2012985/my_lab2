import xadmin
from .models import Laboratory,Device
class LaboratoryAdmin(object):
    pass


class DeviceAdmin(object):
    pass


xadmin.site.register(Laboratory,LaboratoryAdmin)
xadmin.site.register(Device,DeviceAdmin)
