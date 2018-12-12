from django.db import models
# from opertion.models import LessonSubscribe  #
# Create your models here.

from datetime import datetime


class Laboratory(models.Model):
    name = models.CharField(max_length=10, verbose_name="实验室名称")
    locate = models.CharField(default='基础实验楼', max_length=30,verbose_name='实验室位置')
    admin = models.CharField(default='ykk', max_length=10, verbose_name='实验室管理员')
    detail = models.TextField(default='123', verbose_name='实验室介绍')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
    open_start = models.DateTimeField(default=datetime.now, verbose_name="实验室开放时间")
    open_stop = models.DateTimeField(default=datetime.now, verbose_name="实验室开放结束时间")
    capacity = models.IntegerField(default=80, verbose_name="实验室容量")

    class Meta:
            verbose_name = "实验室名称"
            verbose_name_plural = verbose_name

    def __str__(self):
            return self.name


class Desk(models.Model):
    number = models.CharField(max_length=20, verbose_name="实验台编号")
    lab = models.ForeignKey(Laboratory, on_delete=models.CASCADE, verbose_name="所属实验室")
    row = models.IntegerField(blank=True, null=True, verbose_name="横排")
    column = models.IntegerField(blank=True, null=True, verbose_name="竖排")
    available = models.BooleanField(default=True, verbose_name="是否可用")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="购买时间")

    class Meta:
        verbose_name = "实验台"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.number


class Device(models.Model):
    """
    实验仪器
    """
    name = models.CharField(max_length=20, verbose_name="仪器名称")
    kind = models.CharField(max_length=10, verbose_name='仪器属性')
    laboratory = models.ForeignKey(Desk, on_delete=models.CASCADE, verbose_name="所属实验台")
    brand = models.CharField(default='Tektronix', max_length=10, verbose_name='品牌')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="购买时间")
    detail = models.TextField(default='123', verbose_name='仪器说明')
    available = models.BooleanField(default=True, verbose_name="是否可用")

    class Meta:
        verbose_name = "仪器名称"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

