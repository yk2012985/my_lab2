from django.db import models
# Create your models here.
from datetime import datetime


class Laboratory(models.Model):
    name = models.CharField(max_length=10,verbose_name="实验室名称")
    locate = models.CharField(default='基础实验楼', max_length=30,verbose_name='实验室位置')
    admin = models.CharField(default='ykk', max_length=10, verbose_name='实验室管理员')
    detail = models.TextField(default='123', verbose_name='实验室介绍')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")

    class Meta:
            verbose_name = "实验室名称"
            verbose_name_plural = verbose_name

    def __str__(self):
            return self.name


class Device(models.Model):
    name = models.CharField(max_length=20, verbose_name="仪器名称")
    kind = models.CharField(max_length=10,verbose_name='仪器属性')
    laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, verbose_name="信号源所属的实验室")
    brand = models.CharField(default='Tektronix',max_length=10, verbose_name='品牌')
    add_time = models.DateTimeField(default=datetime.now, verbose_name="购买时间")
    detail = models.TextField(default='123', verbose_name='仪器说明')

    class Meta:
        verbose_name = "仪器名称"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# class Oscilloscope(models.Model):
#     name = models.CharField(max_length=20, verbose_name="示波器名称")
#     laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, verbose_name="示波器所属的实验室")
#     brand = models.CharField(default='Tektronix', max_length=10, verbose_name='品牌')
#     add_time = models.DateTimeField(default=datetime.now, verbose_name="购买时间")
#
#     class Meta:
#         verbose_name = "示波器名称"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name
#
#
# class Multimeter(models.Model):
#     name = models.CharField(max_length=20, verbose_name="万用表名称")
#     laboratory = models.ForeignKey(Laboratory, on_delete=models.CASCADE, verbose_name="万用表所属的实验室")
#     brand = models.CharField(default='Tektronix', max_length=10, verbose_name='品牌')
#     add_time = models.DateTimeField(default=datetime.now, verbose_name="购买时间")
#
#     class Meta:
#         verbose_name = "万用表名称"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name