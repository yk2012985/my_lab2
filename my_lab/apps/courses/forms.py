from django import forms
from .models import Course, Lesson, CourseResource


# class UploadFileForm(forms.ModelForm):
#     class Meta:
#         model = CourseResource
#         fields = ['download']#用模型表格来验证表单格式不通过，原因暂时不明
class UploadFileForm(forms.Form):
    name = forms.CharField(required=True)
    upload = forms.FileField(required=True)


# class LessonFieldForm(forms.Form):
#     name = forms.CharField(required=True)
#     detail = forms.CharField(required=True, widget=forms.Textarea)
#
#
# class CourseFieldForm(forms.Form):  # 验证科目信息格式的表单，用这种表单格式验证的方式，可以省去在视图函数中对request.POST.get()的try验证
#     name = forms.CharField(required=True)
#     desc = forms.CharField(max_length=50, required=True, widget=forms.Textarea)
#     detail = forms.CharField(required=True, widget=forms.Textarea)


class CourseFieldForm(forms.ModelForm):  # 模型表格形式
    class Meta:
        model = Course
        fields = ['name', 'detail']


class LessonFieldForm(forms.ModelForm):  # ModelForm的方式
    class Meta:
        model = Lesson
        fields = ['course', 'name', 'detail', 'labs']
