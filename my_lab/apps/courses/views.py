from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import render
from django.http import HttpResponse
from .models import Course, Lesson, CourseResource
from measure.models import Laboratory
from .forms import UploadFileForm, CourseFieldForm, LessonFieldForm, LessonFieldForm
from django.contrib.auth.decorators import login_required
from django.http import FileResponse
from django.contrib import messages  # Django的信息显示框架用于显示登录提示信息
from django.views.generic import ListView  # 引入通用视图
# from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.


# def course_view(request):
#     """
#     科目列表函数
#     """
#     courses = Course.objects.all()
#     course_number = courses.count()
#     # if 'username' in request.session:#这里用了内置的验证函数，两种验证方式都可以
#     if request.user.is_authenticated():
#         return render(request, 'course_list.html', {'courses': courses,
#                                                     'course_number': course_number,
#                                                      }
#                       )
#     else:
#         return render(request, 'login2.html')


#  使用通用视图
class CoursesList(ListView):

    model = Course
    context_object_name = 'courses'  # 为了在前端模板文件中好识别所添加的名字




@login_required(login_url='login')
def course_information(request, course_id):
    """
    科目信息函数
    """

    try:
        course = Course.objects.get(pk=course_id)
    except :
        pass
    lessons = Lesson.objects.filter(course=course)  # 两种查询方式都可以
    files = CourseResource.objects.filter(course=course)
    if 'username' in request.session:
        return render(request, 'course_imfo.html', {'course': course,
                                                    'lessons': lessons,
                                                    'files': files,
                                                    }
                      )
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


@login_required(login_url='login')
def course_edit_page(request, course_id):  # 此函数承担两个任务，添加课目与修改课目，关键看id是否为0
    """
    科目编辑函数1
    """

    if str(course_id) == '0':
        course_form = CourseFieldForm()
        return render(request, 'course_edit.html', {'courseform': course_form})
    else:
        course = Course.objects.get(pk=course_id)
        course_form = CourseFieldForm(instance=course)
        return render(request, 'course_edit.html', {'courseform': course_form,
                                                    'course': course})


# def course_edit_action(request):这种只用函数编辑的方法可行，但不推荐，重复代码量大
#     if request.method == 'POST':
#         course_form = CourseFieldForm(request.POST)  # 验证表单格式
#         course_id = request.POST.get('course_id', '0')  # get方法的第二个参数是默认值
#         if course_form.is_valid():
#             course_id = request.POST.get('course_id', '0')  # get方法的第二个参数是默认值
#             if course_id == '0':
#                 name = request.POST.get('name', '')
#                 desc = request.POST.get('desc', '')
#                 detail = request.POST.get('detail', '')
#                 course = Course(name=name, desc=desc, detail=detail)
#                 course.save()
#                 courses = Course.objects.all()
#                 return render(request, 'course_list.html', {'courses': courses})
#             else:
#                 course = Course.objects.get(pk=course_id)
#                 course.name = request.POST.get('name', '')
#                 course.desc = request.POST.get('desc', '')
#                 course.detail = request.POST.get('detail', '')
#                 course.save()
#                 return render(request, 'course_imfo.html', {'course': course,
#                                                             'name': course.name,
#                                                             'desc': course.desc,
#                                                             'detail': course.detail,
#                                                             'add_time': course.add_time
#                                                             }
#                               )
#         else:
#             course = Course.objects.get(pk=course_id)
#             return render(request, 'course_edit.html', {'course': course
#                                                         }
#                           )
#     else:
#         messages.add_message(request, messages.ERROR, '操作错误，请重试')
#         return render(request, 'teacher_index.html')


def course_edit_action(request):
    """
    科目编辑函数2
    """
    if request.method == 'POST':
        course_form = CourseFieldForm(request.POST)  # 验证表单格式
        course_id = request.POST.get('course_id', '0')  # get方法的第二个参数是默认值
        if course_form.is_valid():
            if course_id == '0':
                course_form.save(commit=True)
            else:
                try:
                    # 以下是第一种方法
                    # course_old = Course.objects.get(pk=course_id)  # 先找到旧的course
                    # course_old.delete()  # 把旧的删除掉
                    # course_form.save(commit=True)  # 新的保存起来
                    # 以下是第二种方法
                    course = Course.objects.get(pk=course_id)  # 找到旧的
                    c = CourseFieldForm(request.POST, instance=course)  # 直接在旧的基础上保存
                    c.save()
                except:
                    messages.add_message(request, messages.WARNING, '没有找到原数据')
            courses = Course.objects.all()
            return render(request, 'courses_list.html', {'courses': courses})
        else:
            messages.add_message(request, messages.WARNING, '格式不符，请重新填写')
            course = Course.objects.get(pk=course_id)
            return render(request, 'course_edit.html', {'course': course
                                                        }
                          )


@login_required(login_url='login')
def lesson_info(request, lesson_id):
    """
    实验课信息函数
    """
    lesson = Lesson.objects.get(pk=lesson_id)
    course = lesson.course
    lab = lesson.labs
    return render(request, 'lesson_info.html', {'lesson': lesson, 'course': course})


@login_required(login_url='login')
def lesson_edit_page(request, lesson_id, course_id):  # 此函数承担两个任务，添加课目与修改课目，关键看id是否为0
    """
    实验课编辑函数1
    """
    course = Course.objects.get(pk=course_id)
    courses = Course.objects.all()
    labs = Laboratory.objects.all()
    if str(lesson_id) == '0':
        lesson_form = LessonFieldForm()
        return render(request, 'lesson_edit.html', {'lessonform': lesson_form,
                                                    'course': course,
                                                    'courses': courses,
                                                    'labs': labs
                                                    }
                      )
    else:
        lesson = Lesson.objects.get(pk=lesson_id)
        lesson_form = LessonFieldForm(instance=lesson)
        return render(request, 'lesson_edit.html', {'lessonform': lesson_form,
                                                    'lesson': lesson,
                                                    'course': course,
                                                    'courses': courses,
                                                    'labs': labs
                                                    }
                      )


def lesson_edit_action(request):  # 原则上这个响应函数及上面的course_edit_action()都要有if request.method==POST这个判断，用来检查
    # 得到的信息是否是通过前端的submit键来得到的，但不知道除了单击submit来传递表单以外还能通过什么方式传递，所以这里先不判断，打个问号。
    # 回答：不通过单击submit还可以通过网址来直接访问页面
    """
    实验课编辑函数2
    """
    if request.method == 'POST':
        lesson_form = LessonFieldForm(request.POST)  # 验证表单格式
        lesson_id = request.POST.get('lesson_id', '0')  # get方法的第二个参数是默认值
        course_id = request.POST.get('course', '')  # 获取下拉菜单的选中值，get方法的第二个参数是默认值
        course = Course.objects.get(pk=course_id)
        lab_id = request.POST.get('labs')
        if lesson_id == '0':
            if lesson_form.is_valid():
                lesson_form.save()
                lessons = Lesson.objects.filter(course__id=course_id)
                return render(request, 'course_imfo.html', {'course': course, 'lessons': lessons})
            else:
                messages.add_message(request, messages.WARNING, '请规范填写')
                courses = Course.objects.all()
                return render(request, 'lesson_edit.html', {'courses': courses})
        else:
            if lesson_form.is_valid():
                try:
                    lesson_old = Lesson.objects.get(pk=lesson_id)
                except:
                    messages.add_message(request, messages.WARNING, '没有找到原数据')
                    courses = Course.objects.all()
                    labs = Laboratory.objects.all()
                    return render(request, 'lesson_edit.html', {'courses': courses, 'labs':labs})
                lesson_old.delete()
                lesson_form.save()
                lessons = Lesson.objects.filter(course__id=course_id)
                course = Course.objects.get(pk=course_id)
                courses = Course.objects.all()
                return render(request, 'course_imfo.html', {'course': course,
                                                            'lessons': lessons,
                                                            'courses': courses
                                                            }
                              )
            else:
                lesson = Lesson.objects.get(pk=lesson_id)
                course = Course.objects.get(pk=course_id)
                courses = Course.objects.all()
                labs = Laboratory.objects.all()
                messages.add_message(request, messages.WARNING, '格式错误，请重新填写')
                return render(request,'lesson_edit.html', {'lesson': lesson,
                                                           'course': course,
                                                           'courses': courses,
                                                           'labs': labs
                                                           }
                              )
    else:
        messages.add_message(request, messages.WARNING, '请正常操作不要乱搞')
        return render(request, 'lesson_edit.html')


@login_required(login_url='login')
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


@login_required(login_url='login')
def upload_file_page(request, course_id):
    """
    科目资料上传函数1
    """
    course = Course.objects.get(pk=course_id)
    course_id = course_id
    return render(request, 'course_resource_upload.html', {'course': course,
                                                           'course_id': course_id})


@login_required(login_url='login')
def upload_file_action(request):
    """
    科目资料上传函数2
    """
    if request.method == 'POST':  # 必须是经过post方法FILES才有数据
        form = UploadFileForm(request.POST, request.FILES)
        course_id = request.POST.get('course_id')
        name = request.POST.get('name')
        course = Course.objects.get(pk=course_id)
        try:
            file = CourseResource.objects.get(name=name)
            messages.add_message(request, messages.WARNING, '该文件已存在，请改用其他名字')
            return render(request, 'course_resource_upload.html', {'course': course})
        except:
            try:
                course = Course.objects.get(pk=course_id)
                if form.is_valid():
                    instance = CourseResource(course=course, name=name, download=request.FILES['upload'])
                    instance.save()
                    lessons = Lesson.objects.filter(course=course)  # 两种查询方式都可以
                    files = CourseResource.objects.filter(course=course)
                    messages.add_message(request, messages.INFO, '文件上传成功')
                    return render(request, 'course_imfo.html', {'course': course,
                                                                'lessons': lessons,
                                                                'files': files
                                                                }
                                  )
                else:
                    messages.add_message(request, messages.ERROR, '文件上传失败')
                    return render(request, 'course_resource_upload.html', {'course': course})
            except:
                messages.add_message(request, messages.ERROR, '文件上传失败')
                return render(request, 'course_resource_upload.html')


@login_required(login_url='login')
def course_file_context(request, file_id):
    """
    科目资料打开函数
    """
    try:
        file = CourseResource.objects.get(pk=file_id)
        location = 'F:\python\work\my_lab\media\course\\'+str(file.name)+'.txt'
        with open(location)as file_object:
            lines = file_object.readlines()
            # context = file_object.read()
            # print(context)
        return render(request, 'course_file.html', {'lines': lines,
                                                    'file': file
                                                    }
                      )
    except:
        messages.add_message(request, messages.ERROR, '找不到文档')
        return render(request, 'course_file.html')


@login_required(login_url='login')
def course_file_download(request, file_id):
    """
    科目资料下载函数
    """
    file = CourseResource.objects.get(pk=file_id)
    # location = 'F:\python\work\my_lab\media\course\\' + str(file.name) + '.txt'
    # with open(location)as file_object:
    #     c = file_object.read()
    return HttpResponse(file.download)  # 直接返回文件用于下载即可
