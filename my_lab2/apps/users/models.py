from django.db import models
from django.contrib.auth.models import AbstractUser, Group
# Create your models here.


class UserProfile(AbstractUser):
    number = models.CharField(max_length=20, verbose_name="号码")
    major = models.CharField(max_length=20, blank=True, null=True, verbose_name="专业")
    school = models.CharField(max_length=30, blank=True, null=True, verbose_name="学院")
    mobile = models.CharField(max_length=11, blank=True, null=True, verbose_name="手机号")
    type = models.CharField(choices=(("teacher", "教师"), ("student", "学生")),
                            default="student", max_length=10)
    groups = models.ManyToManyField(Group, verbose_name="职业")

    class Meta:
        verbose_name = "用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username

