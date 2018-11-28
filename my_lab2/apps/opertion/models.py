from django.db import models
from courses.models import Lesson
from users.models import UserProfile
from measure.models import Laboratory
from datetime import datetime
# Create your models here.





# 实验发布
class LessonPublic(models.Model):
    teacher = models.ForeignKey(UserProfile,null=True, blank=True, verbose_name="实验教师")
    lesson = models.ForeignKey(Lesson, null=True, blank=True, verbose_name="发布实验")
    lab = models.ForeignKey(Laboratory, null=True, blank=True, verbose_name="所在实验室")
    start_time = models.DateTimeField(default=datetime.now, verbose_name="实验开始时间")
    stop_time = models.DateTimeField(default=datetime.now, verbose_name="实验结束时间")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "实验发布"
        verbose_name_plural = verbose_name


# 实验预约
class LessonSubscribe(models.Model):
    student = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name="实验学生")
    lesson = models.ForeignKey(Lesson, null=True, blank=True, verbose_name="预约实验")
    grade = models.IntegerField(default=0, verbose_name="实验分数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "实验预约"
        verbose_name_plural = verbose_name



