from django.shortcuts import render
from django.views.generic.base import View
from courses.models import LessonResource
from courses.forms import LessonPublicForm
from measure.models import Laboratory

from django.urls import reverse
from .models import LessonPublic, LessonSubscribe
from django.http import HttpResponse, HttpResponseRedirect
import json
from datetime import datetime
# Create your views here.

class LessonPublicView(View):
    """
    实验发布函数
    """
    def get(self, request):
        lesson_public_form = LessonPublicForm()
        lesson_public = LessonPublic.objects.filter(teacher=request.user)
        return render(request, 'lesson_public.html', {
            'lesson_public_form': lesson_public_form,
            'lessons': lesson_public
        })


class LessonPublicSubmitView(View):
    """
    实验发布处理函数
    """
    def get(self, request):
        return render(request, "login2.html")

    def post(self, request):
        lesson_public_form = LessonPublicForm(request.POST)
        if lesson_public_form.is_valid():
                lesson_public_form.save(commit=True)
                return HttpResponseRedirect(reverse('teacher_index'))
        else:
            return HttpResponseRedirect(reverse('teacher_index'))


# class LessonPublicEditView(View):
#     """
#     修改发布实验课页
#     """
#     def get(self, request, lesson_id):
#         lesson_public = LessonPublic.objects.get(id=lesson_id)
#         lesson_public_form = LessonPublicForm(instance=lesson_public)
#         return render(request, 'lesson_public.html', {
#             'lesson_public_form': lesson_public_form,
#             'lesson_id': lesson_public.id
#         })


class LessonPublicInfoView(View):
    """
    已发布实验课详情页
    """
    def get(self, request, lesson_id):
        lesson_public = LessonPublic.objects.get(id=lesson_id)
        lesson = lesson_public.lesson
        lesson_resource = LessonResource.objects.filter(lesson=lesson)
        return render(request, 'lesson_info.html', {
            'lesson_public': lesson_public,
            'lesson': lesson,
            'lesson_resource': lesson_resource
        })


class LessonPublicDeleteView(View):
    """
    已发布实验课删除
    """
    def get(self, request, lesson_id):
        LessonPublic.objects.get(id=lesson_id).delete()
        return HttpResponseRedirect(reverse('teacher_index'))


class LabLessonsView(View):
    """
    异步询问实验室实验信息
    """
    def get(self, request):
        return render(request, "login2.html")

    def post(self, request):
        lab_id = request.POST.get("lab", "1") # 传过来的是实验室的id
        input_lab = Laboratory.objects.get(id=lab_id)
        lab_lessons_public = LessonPublic.objects.filter(lab=input_lab).order_by('-add_time')
        lesson_public_list = []
        for lab_lesson_public in lab_lessons_public:
            e = dict(teacher=lab_lesson_public.teacher.username,
                     lesson=lab_lesson_public.lesson.title,
                     lab=lab_lesson_public.lab.name,
                     start_time=lab_lesson_public.start_time.strftime(format('%Y/%m/%d %H:%M')),
                     stop_time=lab_lesson_public.stop_time.strftime(format('%Y/%m/%d %H:%M')),
                     add_time=lab_lesson_public.add_time.strftime(format('%Y/%m/%d %H:%M'))
                     )

            lesson_public_list.append(e)
        test_data = json.dumps(lesson_public_list)
        print(test_data)
        return HttpResponse(test_data, content_type='application/json')


class LabDatePublicView(View):
    """
    异步询问某实验室某个时间的实验发布情况
    """
    def get(self, request):
        return render(request, "login2.html")

    def post(self, request, lab_id):
        input_start_time = request.POST.get("start_time") # 获取用户当前填写的开始时间
        print(input_start_time)

        input_lab = Laboratory.objects.get(id=lab_id) # 获取当前输入的实验室

        test_lessons_public = LessonPublic.objects.filter(lab=input_lab).order_by('start_time')  # 获取该实验室目前实验发布的情况，
                                                                                              # 按照添加事件由近及远排列
        if input_start_time == '': # 没有输入开始时间，返回输入实验室所有实验情况
            lesson_public_list = []
            for lab_lesson_public in test_lessons_public:
                e = dict(teacher=lab_lesson_public.teacher.username,
                         lesson=lab_lesson_public.lesson.title,
                         lab=lab_lesson_public.lab.name,
                         start_time=lab_lesson_public.start_time.strftime(format('%Y/%m/%d %H:%M')),
                         stop_time=lab_lesson_public.stop_time.strftime(format('%Y/%m/%d %H:%M')),
                         add_time=lab_lesson_public.add_time.strftime(format('%Y/%m/%d %H:%M'))
                         )

                lesson_public_list.append(e)
            test_data = json.dumps(lesson_public_list)
            print(test_data)
            return HttpResponse(test_data, content_type='application/json')

        else:
            lesson_time = datetime.strptime(input_start_time,'%Y/%m/%d %H:%M')

            lesson_date = lesson_time.date() # 截取输入实验开始时间的年、月、日
            lab_date_public_list = []

            for lesson_public in test_lessons_public: # 先用开始时间将输入实验室的实验发布进行筛选
                if lesson_public.start_time.date() == lesson_date:
                    lab_date_public_list.append(lesson_public)


            lesson_public_list = []
            for test_lesson_public in lab_date_public_list:
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


class LessonSubscribeView(View):
    """
    学生预约实验
    """
    def get(self, request):
        return render(request, "login2.html")

    def post(self, request):
        lesson_public_id = request.POST.get("id") # 传过来的是预约课程的id
        try:
            lesson_public = LessonPublic.objects.get(id=lesson_public_id)
        except:
            return HttpResponse('{"status":"fail"}', content_type='application/json')
        lesson_subscribe = LessonSubscribe()
        lesson_subscribe.student = request.user
        lesson_subscribe.lesson = lesson_public
        lesson_subscribe.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')



class LessonSubscribeDeleteView(View):
    """
    取消已预约实验课
    """
    def get(self, request, lesson_subscribe_id):
        lesson_subscribed = LessonSubscribe.objects.get(id=lesson_subscribe_id)
        lesson_subscribed.delete()

        return HttpResponseRedirect(reverse('student_index'))

























































