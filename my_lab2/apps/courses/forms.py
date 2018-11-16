from django import forms
from .models import Lesson
from opertion.models import LessonPublic


# class UploadFileForm(forms.ModelForm):
#     class Meta:
#         model = CourseResource
#         fields = ['download']#用模型表格来验证表单格式不通过，原因暂时不明
# 用传统表单实现
class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['title', 'detail', 'course','template']


class LessonPublicForm(forms.ModelForm):
    class Meta:
        model = LessonPublic
        fields = ['lab', 'start_time', 'stop_time']

#
#
# class CourseFieldForm(forms.Form):  # 验证科目信息格式的表单，用这种表单格式验证的方式，可以省去在视图函数中对request.POST.get()的try验证
#     name = forms.CharField(required=True)
#     detail = forms.CharField(required=True, widget=forms.Textarea)


# 用模型表单实现


# class LessonFieldForm(forms.ModelForm):  # ModelForm的方式
#     class Meta:
#         model = Lesson
#         fields = ['course', 'name', 'detail', 'teacher', 'class_time']
