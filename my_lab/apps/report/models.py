from django.db import models

# Create your models here.


class Template(models.Model):
    title = models.CharField(max_length=30, verbose_name="实验标题")
    content = models.TextField(verbose_name="实验内容")

    class Meta:
        verbose_name = "实验模板"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
