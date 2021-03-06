from django.shortcuts import render
from django.views.generic.base import View
from courses.models import LessonResource
from courses.forms import LessonPublicForm
from measure.models import Laboratory, Desk
from users.models import UserProfile

from django.urls import reverse
from .models import LessonPublic, LessonSubscribe, LessonReport
from django.http import HttpResponse, HttpResponseRedirect
import json
from datetime import datetime
# Create your views here.

class LessonPublicDoneView(View):
    """
    所有已完成实验（公共首页）
    """
    def get(self, request):
        lesson_public_done = LessonPublic.objects.filter(complete=True)
        if request.user.type == 'teacher':
            return render(request, 'index_common.html', {
                'lessons': lesson_public_done,
                'part2': 'done',
                'user_type': 'teacher'
            })
        else:
            return render(request, 'index_common.html', {
                'lessons': lesson_public_done,
                'part2': 'done',
                'user_type': 'student'
            })


class LessonPublicUndoneView(View):
    """
    所有未完成实验（公共首页）
    """
    def get(self, request):
        lesson_public_done = LessonPublic.objects.filter(complete=False)
        if request.user.type == 'teacher':
            return render(request, 'index_common.html', {
                'lessons': lesson_public_done,
                'part2': 'undone',
                'user_type': 'teacher'
            })
        else:
            return render(request, 'index_common.html', {
                'lessons': lesson_public_done,
                'part2': 'undone',
                'user_type': 'student'
            })

class LessonPublicPersonalDoneView(View):
    """
    教师个人已完成实验
    """
    def get(self, request):
        lesson_public_done = LessonPublic.objects.filter(teacher=request.user,complete=True)
        return render(request, 'index_teacher.html',{
            'lessons': lesson_public_done,
            'part1': 'personal',
            'part2': 'done'
        })


class LessonPublicPersonalUndoneView(View):
    """
    教师个人未完成实验
    """
    def get(self, request):
        lesson_public_undone = LessonPublic.objects.filter(teacher=request.user,complete=False)
        return render(request, 'index_teacher.html',{
            'lessons': lesson_public_undone,
            'part1': 'personal',
            'part2': 'undone'
        })

class LessonSubscribePersonalDoneView(View):
    """
    学生个人已完成实验
    """
    def get(self, request):
        lesson_subscribe_done = LessonSubscribe.objects.filter(student=request.user,complete=True)
        return render(request, 'index_student.html',{
            'lessons_subscribe_all': lesson_subscribe_done,
            'part1': 'personal',
            'part2': 'done'
        })


class LessonSubscribePersonalUndoneView(View):
    """
    学生个人未完成实验
    """
    def get(self, request):
        lesson_subscribe_undone = LessonSubscribe.objects.filter(student=request.user,complete=False)
        return render(request, 'index_student.html',{
            'lessons_subscribe_all': lesson_subscribe_undone,
            'part1': 'personal',
            'part2': 'undone'
        })





class LabLessondoneView(View):
    """
    实验室所有完成实验
    """
    def get(self, request):
        lab1 = Laboratory.objects.get(id=1)
        lab2 = Laboratory.objects.get(id=2)
        lab1_lesson = LessonPublic.objects.filter(lab=lab1, complete=True)
        lab2_lesson = LessonPublic.objects.filter(lab=lab2, complete=True)
        return render(request, 'lab_index.html', {
            'lab1_lessons': lab1_lesson,
            'lab2_lessons': lab2_lesson,
            'part2': 'done'
        })

class LabLessonUndoneView(View):
    def get(self, request):
        lab1 = Laboratory.objects.get(id=1)
        lab2 = Laboratory.objects.get(id=2)
        lab1_lesson = LessonPublic.objects.filter(lab=lab1, complete=False)
        lab2_lesson = LessonPublic.objects.filter(lab=lab2, complete=False)
        return render(request, 'lab_index.html', {
            'lab1_lessons': lab1_lesson,
            'lab2_lessons': lab2_lesson,
            'part2': 'undone'
        })


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
    已发布实验课详情页(公共的，从公共首页访问某课程得到的详情)
    """
    def get(self, request, lesson_id):
        lesson_public = LessonPublic.objects.get(id=lesson_id)
        lesson = lesson_public.lesson
        lesson_resource = LessonResource.objects.filter(lesson=lesson)
        return render(request, 'lesson_info_common.html', {
            'lesson_public': lesson_public,
            'lesson_resource': lesson_resource
        })


class TeacherLessonPublicInfoView(View):
    """
    教师已发布实验课详情页
    """
    def get(self, request, lesson_id):
        lesson_public = LessonPublic.objects.get(id=lesson_id)
        lesson = lesson_public.lesson
        lesson_resource = LessonResource.objects.filter(lesson=lesson)
        lesson_subscribes = LessonSubscribe.objects.filter(lesson=lesson_public) # 拿到预约此public的所有subscribe
        reports = [] # 用来装填预约此lesson_public的subscribe的所有的report
        for subscribe in lesson_subscribes:

            report = LessonReport.objects.filter(lesson=subscribe) # 注意这里用的是filter，所以report是一个QuerySet,
                                                                    # 不是单个的LessonReport实例，前端页面上要来个双重循环
            reports.append(report)


        return render(request, 'teacher_lesson_info.html', {
            'lesson_public': lesson_public,
            'lesson': lesson,
            'lesson_resource': lesson_resource,
            'lesson_reports': reports
        })


class StudentLessonInfoView(View):
    """
    学生已预约实验课详情页
    """
    def get(self, request, lesson_id):
        lesson_public = LessonPublic.objects.get(id=lesson_id)
        lesson = lesson_public.lesson
        lesson_resource = LessonResource.objects.filter(lesson=lesson)
        lesson_subscribes = LessonSubscribe.objects.filter(lesson=lesson_public) # 拿到预约此public的所有subscribe
        reports = [] # 用来装填预约此lesson_public的subscribe的所有的report
        for subscribe in lesson_subscribes:

            report = LessonReport.objects.filter(lesson=subscribe) # 注意这里用的是filter，所以report是一个QuerySet,
                                                                    # 不是单个的LessonReport实例，前端页面上要来个双重循环
            reports.append(report)


        return render(request, 'student_lesson_subscribe_info.html', {
            'lesson_public': lesson_public,
            'lesson': lesson,
            'lesson_resource': lesson_resource,
            'lesson_reports': reports
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
        lab_lessons_public = LessonPublic.objects.filter(lab=input_lab, complete=False).order_by('-add_time')
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

        test_lessons_public = LessonPublic.objects.filter(lab=input_lab, complete=False).order_by('start_time')  # 获取该实验室目前实验发布的情况，
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


class LabDeskCheckView(View):
    """
    检查实验室有无满员
    """
    def get(self, request):
        return render(request, "login2.html")
    def post(self, request):
        lesson_id = request.POST.get("id",'4') # 这里接到的是lesson_public的id
        lesson_public = LessonPublic.objects.get(id=lesson_id)
        lab = lesson_public.lab
        lab_desks_all = Desk.objects.filter(lab=lab, available=True) # 该实验所在实验室所有可用的实验台

        if lab_desks_all.count() == 0: # 如果可用实验台为0，则返回实验室已满员，无法预约
            return HttpResponse('{"status":"fail"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"success"}', content_type='application/json')


class LabDeskSheetView(View):
    """
    展示实验台页面
    """
    def get(self, request, lesson_id): # 这里接到的是lesson_public的id
        lesson_public = LessonPublic.objects.get(id=lesson_id)
        lab = lesson_public.lab
        lab_desks_all = Desk.objects.filter(lab=lab, available=True)  # 该实验所在实验室所有可用的实验台
        lab_desks_all_list = []  # 建立一个容器来装全部的实验台，便于剔除
        for desk in lab_desks_all:
            lab_desks_all_list.append(desk)

        lab_desks_1 = []
        lab_desks_2 = []
        lab_desks_3 = []
        lab_desks_4 = []
        lab_desks_5 = []

        lesson_subscribes = LessonSubscribe.objects.filter(lesson=lesson_public)  # 拿到该实验目前的全部预约
        subscribed_desks = []  # 定义一个空的列表，用于装已预约出去的实验台
        for subscribe in lesson_subscribes:
            subscribed_desks.append(subscribe.desk)  # 将所有预约出去的试验台装进去

        for desk in lab_desks_all_list:  # 从lab_desks_all_list中剔除掉所有已预约的实验台
            if desk in subscribed_desks:
                lab_desks_all_list.remove(desk)

        # 在剔除已预约实验台后的所有实验台中进行分类
        for desk in lab_desks_all_list:
            if desk.row == 1:
                lab_desks_1.append(desk)
                #lab_desks_all_list.remove(desk)
            elif desk.row == 2:
                lab_desks_2.append(desk)
                #lab_desks_all_list.remove(desk)
            elif desk.row == 3:
                lab_desks_3.append(desk)
                #lab_desks_all_list.remove(desk)
            elif desk.row == 4:
                lab_desks_4.append(desk)
                #lab_desks_all_list.remove(desk)
            else:
                lab_desks_5.append(desk)
                #lab_desks_all_list.remove(desk)
        return render(request, 'lab_desk_sheet.html', {  # 将分好类的实验台传到前端页面
            'lab_desk_1': lab_desks_1,
            'lab_desk_2': lab_desks_2,
            'lab_desk_3': lab_desks_3,
            'lab_desk_4': lab_desks_4,
            'lab_desk_5': lab_desks_5,
            'lesson_id': lesson_id
        })



class LessonSubscribeView(View):
    """
    学生预约实验
    """
    def get(self, request, lesson_id, desk_id):
        lesson_public = LessonPublic.objects.get(id=lesson_id)
        lesson_subscribe = LessonSubscribe()
        lesson_subscribe.student = request.user
        lesson_subscribe.lesson = lesson_public
        desk = Desk.objects.get(id=desk_id)
        lesson_subscribe.desk = desk
        lesson_subscribe.save()
        return HttpResponseRedirect(reverse('student_index'))

    # def post(self, request):
    #     lesson_public_id = request.POST.get("id") # 传过来的是预约课程的id
    #     try:
    #         lesson_public = LessonPublic.objects.get(id=lesson_public_id)
    #     except:
    #         return HttpResponse('{"status":"fail"}', content_type='application/json')
    #     lesson_subscribe = LessonSubscribe()
    #     lesson_subscribe.student = request.user
    #     lesson_subscribe.lesson = lesson_public
    #     lesson_subscribe.save()
    #     return HttpResponse('{"status":"success"}', content_type='application/json')



class LessonSubscribeDeleteView(View):
    """
    取消已预约实验课
    """
    def get(self, request, lesson_subscribe_id):
        lesson_subscribed = LessonSubscribe.objects.get(id=lesson_subscribe_id)
        lesson_subscribed.delete()

        return HttpResponseRedirect(reverse('student_index'))


class ReportResultSaveView(View):
    """
    实验报告结果保存
    """
    def get(self, request):
        return render(request, "login2.html")

    def post(self, request):
        try:
            report_id = request.POST.get("report_id", '1')
            grade = request.POST.get("grade",'0')
            if_com = request.POST.get("complete",'n')
        except:
            return HttpResponse('{"status":"fail"}', content_type='application/json')
        report = LessonReport.objects.get(id=report_id)
        subscribe = report.lesson
        subscribe.grade = grade
        if if_com == 'y':
            subscribe.complete = True
        else:
            subscribe.complete = False
        subscribe.save()
        return HttpResponse('{"status":"success"}', content_type='application/json')

























































