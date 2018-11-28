from django.shortcuts import render
from django.views.generic.base import View
from courses.forms import LessonPublicForm
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import LessonPublic
# Create your views here.

class LessonPublicView(View):
    """
    实验发布函数
    """
    def get(self, request):
        lesson_public_form = LessonPublicForm()
        return render(request, 'lesson_public.html', {
            'lesson_public_form': lesson_public_form,
        })


class LessonPublicSubmitView(View):
    """
    实验发布处理函数
    """
    def get(self, request):
        return render(request, "login2.html")

    def post(self, request):
        lesson_public_id = request.POST.get('lesson_public_id', '0')
        lesson_public_form = LessonPublicForm(request.POST)
        if lesson_public_form.is_valid():
            if lesson_public_id == '0':
                lesson_public_form.save(commit=True)
                return HttpResponseRedirect(reverse('teacher_index'))
            else:
                lesson_public = LessonPublic.objects.get(id=lesson_public_id)
                LessonPublicForm(request.POST, instance=lesson_public).save()
                return HttpResponseRedirect(reverse('teacher_index'))

        else:
            return render(request, 'lesson_public.html', {
                'lesson_public_form': lesson_public_form,
                'msg': "实验课信息填充有误，请重新填写"
            })


class LessonPublicEditView(View):
    """
    修改发布实验课页
    """
    def get(self, request, lesson_id):
        lesson_public = LessonPublic.objects.get(id=lesson_id)
        lesson_public_form = LessonPublicForm(instance=lesson_public)
        return render(request, 'lesson_public.html', {
            'lesson_public_form': lesson_public_form,
            'lesson_id': lesson_public.id
        })


class LessonPublicInfoView(View):
    """
    已发布实验课详情页
    """
    def get(self, request, lesson_id):
        lesson = LessonPublic.objects.get(id=lesson_id)
        return render(request, 'lesson_info.html', {
            'lesson': lesson
        })


class LessonPublicDeleteView(View):
    def get(self, request, lesson_id):
        LessonPublic.objects.get(id=lesson_id).delete()
        return HttpResponseRedirect(reverse('teacher_index'))


class LessonSubscribeView():
    pass
