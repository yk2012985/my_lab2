import xadmin
from xadmin import views


class BaseSetting(object):#自定义主题
    enable_themes = True
    use_bootswatch = True

class GlobalSettings(object):#自定义标题和底栏
    site_title = "南理工实验管理系统1.0后台"
    site_footer = "设计人：ykk"
    menu_style = "accordion"#设置菜单合并



# class EmailVerifyRecordAdmin(object):
#     pass
    #list_display = ['模型字段1'，'模型字段2'...]这句在后台管理系统中会添加选择框，按照列表中给定的字段对类有选择的进行显示
    #search_fild = ['模型字段1'，'模型字段2'...]这句在后台管理系统中会添加搜索框，按照列表中给定的字段对类进行搜索
    #list_filter = ['模型字段1'，'模型字段2'...]这句在后台管理系统中会添加过滤器框，按照列表中给定的字段对类进行过滤
    #如果搜索包含有外键的内容，则列表元素为：外键所在的字段名__外键对应的类的字段名__

# class BannerAdmin(object):
#     pass

# xadmin.site.register(EmailVerifyRecord,EmailVerifyRecordAdmin)
# xadmin.site.register(Banner,BannerAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
