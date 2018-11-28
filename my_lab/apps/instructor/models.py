# Create your models here.
from django.db import models

# Create your models here.


class Class(models.Model):
    name = models.CharField(max_length=20,verbose_name="班级名称")
    number = models.IntegerField(verbose_name="班级人数")


    class Meta:
        verbose_name = "实验班级"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
