from django.db import models
from courses.models import Lesson
from users.models import UserProfile
from measure.models import Laboratory, Desk
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
    complete = models.BooleanField(default=False, verbose_name="是否完成")

    class Meta:
        verbose_name = "实验发布"
        verbose_name_plural = verbose_name


# 实验预约
class LessonSubscribe(models.Model):
    student = models.ForeignKey(UserProfile, null=True, blank=True, verbose_name="实验学生")
    lesson = models.ForeignKey(LessonPublic, null=True, blank=True, verbose_name="预约实验") # 对应已发布的实验课
    desk = models.ForeignKey(Desk, null=True,blank=True, verbose_name="预约实验台") # 对应预约实验的实验室的实验台
    grade = models.IntegerField(default=0, verbose_name="实验分数")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    complete = models.BooleanField(default=False, verbose_name="是否完成")

    class Meta:
        verbose_name = "实验预约"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.lesson.lesson.title


class LessonReport(models.Model):
    """
    实验报告，这个本来是想放在measure里面，但是因为此model引入了measure的models的Laboratory，
    如果再在measure的models中引入这里的LessonSubscribe，则会造成循环引用，无法运行，所以只能将它放在这里
    """
    name = models.CharField(max_length=20, verbose_name="报告标题")
    lesson = models.ForeignKey(LessonSubscribe, verbose_name="所属实验")
    download = models.FileField(upload_to="lesson/report/%Y/%m", verbose_name="报告文本", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
        verbose_name = "实验报告"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

