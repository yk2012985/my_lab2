from django.db import models
from users.models import UserProfile
from measure.models import Laboratory
from datetime import datetime
# Create your models here.


class Course(models.Model):  # 科目由管理员上传
    name = models.CharField(max_length=50, verbose_name="课程名")
    detail = models.TextField(verbose_name="课程说明")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "科目"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Lesson(models.Model):  # 实验课
    title = models.CharField(max_length=100, verbose_name="实验名称")
    course = models.ForeignKey(Course, blank=True, null=True, on_delete=models.CASCADE, verbose_name="所属科目")
    detail = models.TextField(default="", verbose_name="实验说明")
    template = models.FileField(upload_to="lesson/template/%Y/%m",null=True, blank=True, verbose_name="实验模板", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "实验课"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class LessonResource(models.Model):
    name = models.CharField(max_length=20, verbose_name="资料名称")
    lesson = models.ForeignKey(Lesson, null=True, blank=True, verbose_name="所属实验")
    download = models.FileField(upload_to="lesson/resource/%Y/%m", verbose_name="实验资料", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "实验资料"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name





