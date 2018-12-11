from django.views.generic.base import View
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Course, Lesson
from opertion.models import LessonPublic, LessonSubscribe
from users.models import UserProfile
from measure.models import Laboratory
from .forms import LessonForm, LessonPublicForm
from django.contrib import messages  # Django的信息显示框架用于显示登录提示信息
from django.http import HttpResponseRedirect
import json

from datetime import datetime
# Create your views here.
class LessonPublicAllView(View):
    """
    返回所有已发布的实验课
    """
    def get(self, request):
        lesson_public_all = LessonPublic.objects.all()
        return render(request, 'teacher_index.html', {
            'lessons': lesson_public_all
        })


class LessonAddView(View):
    """
    添加新的实验课
    """
    def get(self, request):
        lesson_form = LessonForm()
        return render(request, 'new_lesson.html', {
            'lesson_form': lesson_form
        })


class LessonAddSubmitView(View):
    """
    处理提交的新的实验课表单
    """
    def get(self, request):
        return render(request, "login2.html")

    def post(self, request):
        lesson_id = request.POST.get('lesson_id', '0')
        lesson_form = LessonForm(request.POST)
        if lesson_form.is_valid():
            if lesson_id == '0':
                lesson_form.save(commit=True)
                return HttpResponseRedirect(reverse("teacher_index"))
            else:
                lesson = Lesson.objects.get(id=lesson_id)
                LessonForm(request.POST, instance=lesson).save()  # 直接在旧的基础上保存
                return HttpResponseRedirect(reverse("teacher_index"))

        else:
            return render(request, 'new_lesson.html', {
                'lesson_form': lesson_form,
                'msg': "实验课信息填充有误，请重新填写"
            })

class InputTestView(View):
    """
    测试用
    """
    def get(self, request):
        return render(request, "login2.html")

    def post(self, request, lab_id):
        #input_data = request.POST.get("lab", "0")

        #input_data = request.POST.get("id_lab", "0")
        input_start_time = request.POST.get("start_time")
        print(input_start_time)
        # input_data = request.POST.get("submit_button", "0")
        #input_lab = Laboratory.objects.get(id=input_data)
        input_lab = Laboratory.objects.get(id=lab_id)
        # if input_lab == "电工电子实验室":
            #d = dict(status="呵呵哒")

        test_lessons_public = LessonPublic.objects.filter(lab=input_lab).order_by('-add_time')  # 按照添加事件由近及远排列
        lesson_public_list = []
        for test_lesson_public in test_lessons_public:
            e = dict(teacher=test_lesson_public.teacher.username,
                     lesson=test_lesson_public.lesson.title,
                     lab=test_lesson_public.lab.name,
                     start_time=test_lesson_public.start_time.strftime(format('%Y/%m/%d %H:%M')),
                     stop_time=test_lesson_public.stop_time.strftime(format('%Y/%m/%d %H:%M')),
                     add_time=test_lesson_public.add_time.strftime(format('%Y/%m/%d %H:%M'))
                     )

            lesson_public_list.append(e)
        test_data = json.dumps(lesson_public_list)
        print(test_data)
        return HttpResponse(test_data , content_type='application/json')
            # else:
            #     return HttpResponse('{"status": "fail"}', content_type='application/json')


def lesson_public_json(l):
    """
    测试用
    :param l:
    :return:
    """

    # def student2dict(std):
    #     return {
    #         'name': std.name,
    #         'age': std.age,
    #         'score': std.score
    #     }

    return {
        #'teacher': l.teacher.username,
        'lesson': l.lesson.title,
        'lab': l.lab.name,
        'start_time': l.start_time,
        'stop_time': l.stop_time,
        'add_time': l.add_time
    }


