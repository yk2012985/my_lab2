from django.shortcuts import render
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.views.generic.base import View
from .models import UserProfile
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
                        return HttpResponseRedirect(reverse("course:teacher_index"))
                    elif user.type=="student":
                        return render(request, "index2.html", {

                        })
                    else:
                        return render(request, "index2.html",{"user": request.user})
            else:
                return render(request, "login2.html", {'msg': "用户名或密码错误", "login_form": login_form})

        else:  # 表单格式验证失败直接返回
                # return render(request, "login.html", {"login_form":login_form})#如果表单格式验证不通过，
                # 则返回登陆页面并将login_form返回给前端从而显示其错误信息
                messages.add_message(request, messages.WARNING, '输入格式错误')
                return render(request, "login2.html")



def log_out(request):  # 使用删除session的方式实现注销
    logout(request)
    # if 'username' in request.session:
    #     del request.session["username"]  # 删除session
    messages.add_message(request, messages.INFO, '注销成功')
    return render(request, 'users/templates/login2.html')
    # else:
    #     return render(request, 'login2.html')



def teacher_index(request):
    return render(request, 'users/templates/teacher_index.html')



def student_index(request):
    return render(request, 'users/templates/student_index.html')


