from datetime import datetime
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.


class UserProfile(AbstractUser):  # 管理员
    grade = models.CharField(max_length=10, verbose_name=u"年级")
    major = models.CharField(max_length=50, verbose_name=u"专业")
    type = models.CharField(choices=(("teacher", "教师"), ("student", "学生")),
                            default="student", max_length=10)
    gender = models.CharField(choices=(("male", u"男"), ("female", "女")),
                              default="male", max_length=10)
    number = models.CharField(max_length=20, verbose_name=u"学号")
    mobil = models.CharField(max_length=11, verbose_name=u"手机号")
    image = models.ImageField(blank=True, upload_to="image/%Y/%m", default=u"image/default.png",
                              max_length=100)
    groups = models.ManyToManyField(Group, verbose_name="职业")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

# 模型字段is_stuff表示是否是职员，是职员才可以登录后台管理系统，这里只能登录，若想修改东西还要赋值权限，否则不能修。超级用户不受此限制







# class EmailVerifyRecord(models.Model):
#     code = models.CharField(max_length=20,verbose_name=u"验证码")
#     email = models.EmailField(max_length=50,verbose_name=u"邮箱")
#     send_type = models.CharField(choices=(("register",u"注册"),
#                                           ("forget",u"找回密码"),)
#                                  ,max_length=10,verbose_name='发送方式')
#     send_time = models.DateTimeField(default=datetime.now,verbose_name='发送时间')#注意这里要把date.now后面默认的括号去掉，
#                                                       # 否则默认时间是项目编译的时间，
#                                                       #  去掉后则是根据class实例化的时间作为默认时间
#     class Meta:
#         verbose_name = "邮箱验证码"
#         verbose_name_plural = verbose_name
#
#
# class Banner(models.Model):
#     title = models.CharField(max_length=100,verbose_name="标题")
#     image = models.ImageField(upload_to="banner/%Y/%m",verbose_name="轮播图",
#                               max_length=100)
#     url = models.URLField(max_length=200,verbose_name="访问地址")
#     index = models.IntegerField(default=100,verbose_name="顺序")
#     add_time = models.DateTimeField(default=datetime.now,verbose_name="添加时间")
#
#     class Meta:
#         verbose_name = "轮播图"
#         verbose_name_plural = verbose_name
