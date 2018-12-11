from django.shortcuts import render
from django.shortcuts import render
from opertion.models import LessonPublic, LessonSubscribe
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from .models import UserProfile
from measure.models import Laboratory
from .forms import LoginForm, RegisterForm
from django.contrib import messages  # Django的信息显示框架用于显示登录提示信息
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
# Create your views here.

class IndexView(View):
    def get(self, request):
        user = request.user
        return render(request, 'index2.html',{
            'user': user
        }
                      )

    # if request.user.is_authenticated:  # 如果函数头前没有加登录装饰器，这个验证有必要存在，但没有也不影响后面的数据取出
    #     username = request.user.username  # 使用内置的登录函数可以这样获得登录用户的全部数据放到username中
    #     user = UserProfile.objects.get(username=username)
    #     # user = UserProfile.objects.get(grade=1)#这里想要验证一下是不是user包含了用户的全部数据
    #     return render(request, 'index2.html', {'username': user.username})
    # else:
    #     return render(request, 'login2.html')


class LoginView(View):  # 我们在这里重构Django的View类，重写get和post方法，
    # Django的View会根据前段的方法类型（get或者是post）自动调用不同的方法来应对，
    # 这里我们重写了get和post方法，就减少了我们自定义登陆函数的代码量推荐使用这种
    # 重写系统方法的范式

    def get(self, request):
        return render(request, "login2.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():  # 这里让表单验证函数先验证一下表单的格式是否正确，
            # 如果正确再开始查询数据库进行下面真正的验证，从而减轻数据库的负担
            user_name = request.POST.get("username", "")
            pass_word = request.POST.get("password", "")
            user = authenticate(username=user_name, password=pass_word)

            if user is not None:
                    request.session['username'] = user_name
                    request.session['password'] = pass_word  # 将用户名和密码写入session，用于验证
                    login(request, user)
                    user = UserProfile.objects.get(username=user_name)
                    if user.type=="teacher":
                        return HttpResponseRedirect(reverse("teacher_index"))
                    elif user.type=="student":
                        return HttpResponseRedirect(reverse("student_index"))
                    else:
                        return render(request, "index2.html",{"user": request.user})
            else:
                return render(request, "login2.html", {'msg': "用户名或密码错误", "login_form": login_form})

        else:  # 表单格式验证失败直接返回
                # return render(request, "login.html", {"login_form":login_form})#如果表单格式验证不通过，
                # 则返回登陆页面并将login_form返回给前端从而显示其错误信息
                messages.add_message(request, messages.WARNING, '输入格式错误')
                return render(request, "login2.html")


class IndexCommonView(View):
    """
    公共首页,默认选择全部实验课
    """
    def get(self, request):


        lesson_subscribe_all = LessonSubscribe.objects.filter(student=request.user,complete=False)
        if request.user.type == 'teacher':
            lesson_public_all = LessonPublic.objects.all()
            return render(request, 'index_common.html', {
                'lessons': lesson_public_all,
                'part2': 'all',
                'user_type':'teacher'
            })
        else:
            lesson_public_all = LessonPublic.objects.filter(complete=False)
            return render(request, 'index_common.html', {
                'lessons': lesson_public_all,
                'lessons_subscribed_all': lesson_subscribe_all,
                'part2': 'all',
                'user_type': 'student'

            })


class LabIndexView(View):
    """
    实验室信息页,默认选择全部实验课
    """
    def get(self, request):
        lab1 = Laboratory.objects.get(id=1)
        lab2 = Laboratory.objects.get(id=2)
        lab1_lesson = LessonPublic.objects.filter(lab=lab1)
        lab2_lesson = LessonPublic.objects.filter(lab=lab2)
        if(request.user.type == 'teacher'):
            return render(request, 'lab_index.html', {
                'lab1_lessons': lab1_lesson,
                'lab2_lessons': lab2_lesson,
                'part2': 'all',
                'user_type': 'teacher'
            })
        else:
            return render(request, 'lab_index.html', {
                'lab1_lessons': lab1_lesson,
                'lab2_lessons': lab2_lesson,
                'part2': 'all',
                'user_type': 'student'
            })



class TeacherIndexView(View):
    """
    教师首页,默认选择个人全部实验课
    """
    def get(self, request):
        # courses = Course.objects.all()
        if request.user.type == 'teacher':
            name = request.user.username
            # teacher = UserProfile.objects.get(user=request.user)
            lesson_public = LessonPublic.objects.filter(teacher=request.user)

            lessons = []  # 用于装发布的lesson，并没有用到
            for lesson in lesson_public:
                lessons.append(lesson.lesson)

            # return render(request, 'teacher_index.html', {
            #     'lessons': lesson_public
            # })
            return render(request, 'index_teacher.html', {
                'lessons': lesson_public,
                'part2': 'all'
            })
        else:
            logout(request)
            return render(request, "login2.html", {}) # 等到设置好logout后，将这里修改掉，先注销再返回登录页


class StudentIndexView(View):
    """
    学生首页
    """
    def get(self, request):
        # courses = Course.objects.all()
        if request.user.type == 'student':
            name = request.user.username
            # teacher = UserProfile.objects.get(user=request.user)
            #lessons_public_all = LessonPublic.objects.all() # 全部已发布的实验课
            lessons_subscribe_all = LessonSubscribe.objects.filter(student=request.user) # 全部已预约的实验课
            lessons = []  # 用于装已预约的LessonPublic
            for lesson in lessons_subscribe_all:
                lessons.append(lesson.lesson) # 注意lesson_subscribe中的lesson对应的是LessonPublic
            return render(request, 'index_student.html', {
                'lessons_subscribe_all': lessons_subscribe_all,
                'part1': 'all',
                'part2': 'all'
            })
        else:
            logout(request)
            return render(request, "login2.html", {}) # 等到设置好logout后，将这里修改掉，先注销再返回登录页


class LogoutView(View):
    """
    用户注销
    """
    def get(self, request):
        logout(request)
        return render(request, 'login2.html')
