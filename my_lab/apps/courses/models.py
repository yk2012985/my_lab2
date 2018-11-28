# Create your models here.
from datetime import datetime
from django.db import models
from measure.models import Laboratory  # 引入实验室和实验课多对多连接
from users.models import UserProfile


class Lesson(models.Model):  # 实验课
    # course = models.ForeignKey(Course, on_delete=models.CASCADE,verbose_name="实验所对应的科目")
    name = models.CharField(max_length=100, verbose_name="实验名称")

    student = models.ManyToManyField(UserProfile, through='Course')

    detail = models.TextField(verbose_name="实验要求")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    labs = models.ManyToManyField(Laboratory, verbose_name="实验室")

    class Meta:
        verbose_name = "实验课"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Course(models.Model):  # 科目
    name = models.CharField(max_length=50, verbose_name="课程名")
    desc = models.CharField(max_length=300, verbose_name="课程描述")
    detail = models.TextField(verbose_name="课程说明")
    student = models.IntegerField(default=0, verbose_name="学习人数")
    click_nums = models.IntegerField(default=0, verbose_name="课程点击量")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    lesson = models.ForeignKey(Lesson, blank=True, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, blank=True,null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "科目"
        verbose_name_plural = verbose_name
        ordering = ['-name']

    def __str__(self):
        return self.name


class LessonFile(models.Model):  # 实验课资料
    lesson = models.ForeignKey(Lesson, verbose_name="实验课")
    name = models.CharField(max_length=100, verbose_name="实验资料名称")
    download = models.FileField(upload_to="course/resource/%Y/%m",
                                verbose_name="实验资料", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "实验资料"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class CourseResource(models.Model):  # 科目资源
    course = models.ForeignKey(Course, verbose_name="资料所对应的科目")
    name = models.CharField(max_length=100, verbose_name="资料名称")
    download = models.FileField(upload_to="course",
                                verbose_name="科目资料", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "科目资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
        # return self.download #不能直接用download字段，xadmin无法直接显示，只能额外给文件添加文件名
