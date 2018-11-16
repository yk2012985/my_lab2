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

from datetime import datetime
# Create your views here.


class TeacherIndexView(View):
    """
    教师首页
    """
    def get(self, request):
        # courses = Course.objects.all()
        name = request.user.username
        # teacher = UserProfile.objects.get(user=request.user)
        lesson_public = LessonPublic.objects.filter(teacher=request.user)
        lessons = []  # 用于装发布的lesson
        for lesson in lesson_public:
            lessons.append(lesson.lesson)
        return render(request, 'teacher_index.html', {
            'lessons': lesson_public
        })


class LessonPublicView(View):
    """
    实验发布函数
    """
    def get(self, request):
        lesson_form = LessonForm()
        lesson_public_form = LessonPublicForm()
        return render(request, 'lesson_public.html', {
            'lesson_form': lesson_form,
            'lesson_public_form': lesson_public_form
        })


class LessonPublicSubmitView(View):
    """
    实验发布处理函数
    """
    def get(self, rquest):
        return render(rquest, "login2.html")

    def post(self, request):
        lesson_form = LessonForm(request.POST)
        lesson_public_form = LessonPublicForm(request.POST)
        if lesson_form.is_valid():
            lesson = lesson_form.save(commit=True)

            if lesson_public_form.is_valid():
                lesson_public = LessonPublic()
                lesson_public.teacher = request.user  # 先判定用户已登陆
                lesson_public.lesson = lesson
                lesson_public.lab = lesson_public_form.lab
                lesson_public.start_time = lesson_public_form.start_time
                lesson_public.stop_time = lesson_public_form.stop_time
                lesson_public.add_time = datetime.now
                lesson_public.save()
                return HttpResponseRedirect(reverse('teacher_index'))
            else:
                return render(request, 'lesson_public.html', {
                    'lesson_form': lesson_form,
                    'lesson_public_form': lesson_public_form,
                    'msg': "实验课发布信息填充有误，请重新填写"
                })

        else:
            return render(request, 'lesson_public.html', {
                'lesson_form': lesson_form,
                'lesson_public_form': lesson_public_form,
                'msg': "实验课信息填充有误，请重新填写"
            })












def courses_list(request):
    courses = Course.objects.all()
    if request.user.type == 'teacher':
        teacher = 'true'
        return render(request, 'courses/templates/courses_list.html', {'courses': courses,
                                                                       'teacher': teacher,
                                                                       }
                      )
    else:
        return render(request, 'courses/templates/courses_list.html', {'courses': courses
                                                                       }
                      )



def course_information(request, course_id):
    """
    科目信息函数
    """

    try:
        course = Course.objects.get(pk=course_id)
    except :
        pass
    lessons = Lesson.objects.filter(course=course)  # 两种查询方式都可以
    # files = CourseResource.objects.filter(course=course)
    if 'username' in request.session:
        return render(request, 'courses/templates/course_imfo.html', {'course': course,
                                                                      'lessons': lessons,
                                                                       # 'files': files,
                                                                      }
                      )
        # return HttpResponseRedirect(reverse('course:course_info', args=(course.id,)))  # 目前还不能用，找原因，重定向次数过多
    else:
        return render(request, 'login2.html')


def course_delete(request, course_id):
    """
    科目删除函数
    """
    course = Course.objects.get(pk=course_id)
    course.delete()
    courses = Course.objects.all()
    return render(request, "courses_list.html", {'courses': courses})



# def course_edit_page(request, course_id):  # 此函数承担两个任务，添加课目与修改课目，关键看id是否为0
#     """
#     科目编辑函数1
#     """
#
#     if str(course_id) == '0':
#         course_form = CourseFieldForm()
#         return render(request, 'courses/templates/course_edit.html', {'courseform': course_form})
#     else:
#         course = Course.objects.get(pk=course_id)
#         course_form = CourseFieldForm(instance=course)
#         return render(request, 'courses/templates/course_edit.html', {'courseform': course_form,
#                                                                       'course': course
#                                                                       }
#                       )


# def course_edit_action(request):
#     """
#     科目编辑函数2
#     """
#     if request.method == 'POST':
#         course_form = CourseFieldForm(request.POST)  # 验证表单格式
#         course_id = request.POST.get('course_id', '0')  # get方法的第二个参数是默认值
#         if course_form.is_valid():
#             if course_id == '0':
#                 course_form.save(commit=True)
#             else:
#                 try:
#                     # 以下是第一种方法
#                     # course_old = Course.objects.get(pk=course_id)  # 先找到旧的course
#                     # course_old.delete()  # 把旧的删除掉
#                     # course_form.save(commit=True)  # 新的保存起来
#                     # 以下是第二种方法
#                     course = Course.objects.get(pk=course_id)  # 找到旧的
#                     c = CourseFieldForm(request.POST, instance=course)  # 直接在旧的基础上保存
#                     c.save()
#                 except:
#                     messages.add_message(request, messages.WARNING, '没有找到原数据')
#             courses = Course.objects.all()
#             return HttpResponseRedirect(reverse('course:course_list'))  # 用这种重定向的方式返回更好
#             # return render(request, 'courses_list.html', {'courses': courses})
#         else:
#             messages.add_message(request, messages.WARNING, '格式不符，请重新填写')
#             course = Course.objects.get(pk=course_id)
#             return HttpResponseRedirect(reverse('course:course_edit_page', args=(course.id,)))



def lesson_info(request, lesson_id):
    """
    实验课信息函数
    """
    lesson = Lesson.objects.get(pk=lesson_id)
    course = lesson.course
    labs = lesson.labs.all()
    for lab in labs:
        print(lab.name)
    if request.user.type == 'student':
        student = 'true'
        return render(request, 'courses/templates/lesson_info.html', {'lesson': lesson,
                                                                      'course': course,
                                                                      'labs': labs,
                                                                      'student': student,
                                                                      }
                      )
    else:
        teacher = 'true'
        students = lesson.students.all()
        for student in students:
            print(student.username)
        return render(request, 'lesson_info.html', {'lesson': lesson,
                                                    'course': course,
                                                    'labs': labs,
                                                    'teacher': teacher,
                                                    'students': students,
                                                    }
                      )



# def lesson_edit_page(request, lesson_id, course_id):  # 此函数承担两个任务，添加课目与修改课目，关键看id是否为0
#     """
#     实验课编辑函数1
#     """
#     course = Course.objects.get(pk=course_id)
#     courses = Course.objects.all()
#     labs = Laboratory.objects.all()
#     if str(lesson_id) == '0':
#         lesson_form = LessonFieldForm()
#         return render(request, 'courses/templates/lesson_edit.html', {
#                                                     # 'lessonform': lesson_form,
#                                                     'course': course,
#                                                     'courses': courses,
#                                                     'labs': labs
#                                                     }
#                       )
#     else:
#         lesson = Lesson.objects.get(pk=lesson_id)
#         # lesson_form = LessonFieldForm(instance=lesson)
#         return render(request, 'lesson_edit.html', {
#                                                     # 'lessonform': lesson_form,
#                                                     'lesson': lesson,
#                                                     'course': course,
#                                                     'courses': courses,
#                                                     'labs': labs
#                                                     }
#                       )


# def lesson_edit_action(request):  # 原则上这个响应函数及上面的course_edit_action()都要有if request.method==POST这个判断，用来检查
#     # 得到的信息是否是通过前端的submit键来得到的，但不知道除了单击submit来传递表单以外还能通过什么方式传递，所以这里先不判断，打个问号。
#     # 回答：不通过单击submit还可以通过网址来直接访问页面
#     """
#     实验课编辑函数2
#     """
#     if request.method == 'POST':
#         lesson_form = LessonFieldForm(request.POST)  # 验证表单格式
#         lesson_id = request.POST.get('lesson_id', '0')  # get方法的第二个参数是默认值
#         course_id = request.POST.get('course', '')  # 获取下拉菜单的选中值，get方法的第二个参数是默认值
#         course = Course.objects.get(pk=course_id)
#         # lesson = Lesson.objects.get(pk=lesson_id)
#         lab_id = request.POST.get('labs')
#         if lesson_id == '0':
#             if lesson_form.is_valid():
#                 # lesson = lesson_form.save()
#                 name = request.POST.get('name', '')
#                 detail = request.POST.get('detail', '')
#                 course_id = request.POST.get('course', '')
#                 course = Course.objects.get(pk=course_id)
#                 teacher = request.POST.get('teacher', '')
#
#                 start_year = int(request.POST.get('start_year', '2018'))
#                 start_month = int(request.POST.get('start_month', '3'))
#                 start_day = int(request.POST.get('start_day', '1'))
#                 start_hour = int(request.POST.get('start_hour', '8'))
#                 start_min = int(request.POST.get('start_min', '0'))
#                 start_datetime = datetime(start_year, start_month, start_day, start_hour, start_min)
#                 print(start_datetime)
#
#                 stop_hour = int(request.POST.get('stop_hour', '20'))
#                 stop_min = int(request.POST.get('stop_min', '30'))
#                 stop_datetime = datetime(start_year, start_month, start_day, stop_hour, stop_min)
#                 print(stop_datetime)
#
#                 if stop_datetime < start_datetime:  # 先判断时间是否符合逻辑
#                     courses = Course.objects.all()
#                     labs = Laboratory.objects.all()
#                     messages.add_message(request, messages.ERROR, '实验课时间错误，请重新选择')
#
#                     return render(request, 'lesson_edit.html', {'courses': courses,
#                                                                 'labs': labs
#                                                                 }
#                                   )
                   # return HttpResponseRedirect(reverse('course:lesson_edit_page', args=(lesson_id,course.id)))
    # 符合逻辑,和实验室时间比较
    #
    #             lab_ids = request.POST.getlist('lab_ids')
    #             for id_get in lab_ids:  # 检测是否可以正常得到实验室的id
    #                 print(id_get)
    #             labs_get = []
    #             for lab_id in lab_ids:  # 获取实验室列表
    #                 lab = Laboratory.objects.get(pk=lab_id)
    #                 print(lab.name)
    #                 labs_get.append(lab)  # 获得所选择的实验室列表
    #             courses = Course.objects.all()
    #             labs = Laboratory.objects.all()  # 所有实验室的列表，用于出错时返回用
    #             for lab in labs_get:  # 先和每个实验室的开放时间比较
    #                 if start_datetime < lab.open_start:
    #                     messages.add_message(request, messages.ERROR, '开始时间早于实验室 %s 开放时间' % lab.name)
    #                     return render(request, 'lesson_edit.html', {'courses': courses,
    #                                                                 'labs': labs
    #                                                                 }
    #
    #                                   )
    #                 elif stop_datetime > lab.open_stop:
    #                     messages.add_message(request, messages.ERROR, '开始时间晚于实验室 %s 关闭时间' % lab.name)
    #                     return render(request, 'lesson_edit.html', {'courses': courses,
    #                                                                 'labs': labs
    #                                                                 }
    #                                   )
    #                    # return HttpResponseRedirect(reverse('course:lesson_edit_page', args=(lesson.id,course.id)))
    #                 else:  # 没有和该实验室的时间冲突，接下来和该实验室的所有实验课比较
    #                     lessons_of_lab = lab.lesson_set.all()  # 获取该实验室的所有实验课
    #                     for lesson in lessons_of_lab:  # 输出选中实验室已有的课程，可以正常输出
    #                         print(lesson.name)
    #                     if lessons_of_lab is not None:  #
    #                         for lesson in lessons_of_lab:
    #                             # if start_datetime <= lesson.lesson_start and stop_datetime >= lesson.lesson_stop:
    #                             if not(start_datetime >= lesson.lesson_stop or stop_datetime <= lesson.lesson_start):
    #                                 courses = Course.objects.all()
    #                                 labs = Laboratory.objects.all()
    #                                 messages.add_message(request, messages.ERROR, '实验时间与实验室 %s的 %s 时间冲突'
    #                                                      % (lab.name, lesson.name))
    #                                 return render(request, 'lesson_edit.html', {'courses': courses,
    #                                                                             'labs': labs
    #                                                                             }
    #                                               )
    #                                 # return HttpResponseRedirect(
    #                                 #     reverse('course:lesson_edit_page', args=(lesson.id,course.id)))
    #
    #                         lesson = Lesson(name=name, detail=detail, course=course, teacher=teacher,
    #                                         lesson_start=datetime(start_year, start_month, start_day,
    #                                                               start_hour, start_min),
    #                                         lesson_stop=datetime(start_year, start_month, start_day, stop_hour,
    #                                                              stop_min)
    #                                         )
    #                         lesson.save()  # 先保存lesson才能添加laboratory
    #                         # lab_id = request.POST.get('labs', '')
    #                         # laboratory = Laboratory.objects.get(pk=lab_id)
    #
    #                         lesson.labs.set(labs_get)
    #                         lessons = Lesson.objects.filter(course__id=course_id)
    #                         return render(request, 'course_imfo.html', {'course': course, 'lessons': lessons})
    #                     else:
    #                         lesson = Lesson(name=name, detail=detail, course=course, teacher=teacher,
    #                                         lesson_start=datetime(start_year, start_month, start_day,
    #                                                               start_hour, start_min),
    #                                         lesson_stop=datetime(start_year, start_month, start_day, stop_hour,
    #                                                              stop_min)
    #                                         )
    #                         lesson.save()  # 先保存lesson才能添加laboratory
    #                         # lab_id = request.POST.get('labs', '')
    #                         # laboratory = Laboratory.objects.get(pk=lab_id)
    #
    #                         lesson.labs.set(labs)
    #                         lessons = Lesson.objects.filter(course__id=course_id)
    #                         return render(request, 'course_imfo.html', {'course': course, 'lessons': lessons})
    #         else:
    #             messages.add_message(request, messages.WARNING, '请规范填写')
    #             courses = Course.objects.all()
    #             labs = Laboratory.objects.all()
    #             return render(request, 'lesson_edit.html', {'courses': courses,
    #                                                         'labs': labs
    #                                                         }
    #                           )
    #            # return HttpResponseRedirect(reverse('course:lesson_edit_page', args=(lesson.id,course.id)))
    #     else:
    #         if lesson_form.is_valid():
    #             try:
    #                 lesson_old = Lesson.objects.get(pk=lesson_id)
    #             except:
    #                 messages.add_message(request, messages.WARNING, '没有找到原数据')
    #                 courses = Course.objects.all()
    #                 labs = Laboratory.objects.all()
    #                 return render(request, 'lesson_edit.html', {'courses': courses, 'labs': labs})
    #                # return HttpResponseRedirect(reverse('course:lesson_edit_page', args=(lesson.id,course.id)))
    #             lesson_old.delete()  # 删除旧的数据，这种方法可行，但会浪费id，故不采用
    #             name = request.POST.get('name', '')
    #             detail = request.POST.get('detail', '')
    #             course_id = request.POST.get('course', '')
    #             course = Course.objects.get(pk=course_id)
    #             teacher = request.POST.get('teacher', '')
    #
    #             start_year = int(request.POST.get('start_year', '2018'))
    #             start_month = int(request.POST.get('start_month', '3'))
    #             start_day = int(request.POST.get('start_day', '1'))
    #             start_hour = int(request.POST.get('start_hour', '8'))
    #             start_min = int(request.POST.get('start_min', '0'))
    #             start_datetime = datetime(start_year, start_month, start_day, start_hour, start_min)
    #             print(start_datetime)
    #
    #             stop_hour = int(request.POST.get('stop_hour', '20'))
    #             stop_min = int(request.POST.get('stop_min', '30'))
    #             stop_datetime = datetime(start_year, start_month, start_day, stop_hour, stop_min)
    #             print(stop_datetime)
    #
    #             if stop_datetime < start_datetime:  # 先判断时间是否符合逻辑
    #                 courses = Course.objects.all()
    #                 labs = Laboratory.objects.all()
    #                 messages.add_message(request, messages.ERROR, '实验课时间错误，请重新选择')
    #                 return render(request, 'lesson_edit.html', {'courses': courses,
    #                                                             'labs': labs
    #                                                             }
    #                               )
    #                # return HttpResponseRedirect(reverse('course:lesson_edit_page', args=(course.id, lesson_id)))
    #             # 符合逻辑,和实验室时间比较
    #
    #             lab_ids = request.POST.getlist('lab_ids')
    #             for id_get in lab_ids:  # 检测是否可以正常得到实验室的id
    #                 print(id_get)
    #             labs_get = []
    #             for lab_id in lab_ids:  # 获取实验室列表
    #                 lab = Laboratory.objects.get(pk=lab_id)
    #                 print(lab.name)
    #                 labs_get.append(lab)  # 获得所选择的实验室列表
    #             courses = Course.objects.all()
    #             labs = Laboratory.objects.all()  # 所有实验室的列表，用于出错时返回用
    #             for lab in labs_get:  # 先和每个实验室的开放时间比较
    #                 if start_datetime < lab.open_start:
    #                     messages.add_message(request, messages.ERROR, '开始时间早于实验室 %s 开放时间' % lab.name)
    #                     return render(request, 'lesson_edit.html', {'courses': courses,
    #                                                                 'labs': labs
    #                                                                 }
    #                                   )
    #                 elif stop_datetime > lab.open_stop:
    #                     messages.add_message(request, messages.ERROR, '开始时间晚于实验室 %s 关闭时间' % lab.name)
    #                     return render(request, 'lesson_edit.html', {'courses': courses,
    #                                                                 'labs': labs
    #                                                                 }
    #                                   )
    #                    # return HttpResponseRedirect(reverse('course:lesson_edit_page', args=(lesson.id,course.id)))
    #                 else:  # 没有和该实验室的时间冲突，接下来和该实验室的所有实验课比较
    #                     lessons_of_lab = lab.lesson_set.all()  # 获取该实验室的所有实验课
    #                     for lesson in lessons_of_lab:  # 输出选中实验室已有的课程，可以正常输出
    #                         print(lesson.name)
    #                     if lessons_of_lab is not None:  #
    #                         for lesson in lessons_of_lab:
    #                             # if start_datetime <= lesson.lesson_start and stop_datetime >= lesson.lesson_stop:
    #                             if not (start_datetime >= lesson.lesson_stop or stop_datetime <= lesson.lesson_start):
    #                                 courses = Course.objects.all()
    #                                 labs = Laboratory.objects.all()
    #                                 messages.add_message(request, messages.ERROR, '实验时间与实验室 %s的 %s 时间冲突'
    #                                                      % (lab.name, lesson.name))
    #                                 return render(request, 'lesson_edit.html', {'courses': courses,
    #                                                                             'labs': labs
    #                                                                             }
    #                                               )
    #                                 # return HttpResponseRedirect(
    #                                 #     reverse('course:lesson_edit_page', args=(lesson.id,course.id)))
    #                         lesson = Lesson(name=name, detail=detail, course=course, teacher=teacher,
    #                                         lesson_start=datetime(start_year, start_month, start_day,
    #                                                               start_hour, start_min),
    #                                         lesson_stop=datetime(start_year, start_month, start_day, stop_hour,
    #                                                              stop_min)
    #                                         )
    #                         lesson.save()  # 先保存lesson才能添加laboratory
    #                         # lab_id = request.POST.get('labs', '')
    #                         # laboratory = Laboratory.objects.get(pk=lab_id)
    #
    #                         lesson.labs.set(labs_get)
    #                         lessons = Lesson.objects.filter(course__id=course_id)
    #                         return render(request, 'course_imfo.html', {'course': course, 'lessons': lessons})
    #                     else:
    #                         lesson = Lesson(name=name, detail=detail, course=course, teacher=teacher,
    #                                         lesson_start=datetime(start_year, start_month, start_day,
    #                                                               start_hour, start_min),
    #                                         lesson_stop=datetime(start_year, start_month, start_day, stop_hour,
    #                                                              stop_min)
    #                                         )
    #                         lesson.save()  # 先保存lesson才能添加laboratory
    #                         # lab_id = request.POST.get('labs', '')
    #                         # laboratory = Laboratory.objects.get(pk=lab_id)
    #
    #                         lesson.labs.set(labs)
    #                         lessons = Lesson.objects.filter(course__id=course_id)
    #                         return render(request, 'course_imfo.html', {'course': course, 'lessons': lessons})
    #         else:
    #             lesson = Lesson.objects.get(pk=lesson_id)
    #             course = Course.objects.get(pk=course_id)
    #             courses = Course.objects.all()
    #             labs = Laboratory.objects.all()
    #             messages.add_message(request, messages.WARNING, '格式错误，请重新填写')
    #             return render(request, 'lesson_edit.html', {'lesson': lesson,
    #                                                         'course': course,
    #                                                         'courses': courses,
    #                                                         'labs': labs
    #                                                         }
    #                           )
    #            # return HttpResponseRedirect(reverse('course:lesson_edit_page', args=(lesson.id,course.id)))
    # else:
    #     messages.add_message(request, messages.WARNING, '请正常操作不要乱搞')
    #     return render(request, 'lesson_edit.html')
#  问题：填写错误后连原有的数据也删掉了



def lesson_delete(request, course_id, lesson_id):
    """
    实验课删除函数
    """
    lesson = Lesson.objects.get(pk=lesson_id)
    lesson.delete()
    lessons = Lesson.objects.filter(course__id=course_id)
    course = Course.objects.get(pk=course_id)
    return render(request, 'course_imfo.html', {'course': course,
                                                # 'name': course.name,
                                                # 'desc': course.desc,
                                                # 'detail': course.detail,
                                                # 'add_time': course.add_time
                                                'lessons': lessons
                                                }
                  )



def lesson_select(request, lesson_id):

    if request.user.type == 'student':
        lesson = Lesson.objects.get(pk=lesson_id)
        student_id = request.user.id
        student = UserProfile.objects.get(pk=student_id)
        lesson.students.add(student)
        lessons_personal = Lesson.objects.filter(students=student_id)
        return render(request, 'courses/templates/student_personal_lesson.html', {'lessons_personal': lessons_personal
                                                                                  }
                      )



def lesson_cancel_select(request, lesson_id):

    if request.user.type == 'student':
        lesson = Lesson.objects.get(pk=lesson_id)
        student_id = request.user.id
        student = UserProfile.objects.get(pk=student_id)
        lesson.students.remove(student)
        lessons_personal = Lesson.objects.filter(students=student_id)
        return render(request, 'student_personal_lesson.html', {'lessons_personal': lessons_personal
                                                                }
                      )



def student_personal_lesson(request):
    if request.user.type == 'student':
        student_id = request.user.id
        lessons_personal = Lesson.objects.filter(students=student_id)
        return render(request, 'student_personal_lesson.html', {'lessons_personal': lessons_personal
                                                                }
                      )

