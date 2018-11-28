from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password  # 用来给明文密码加密存到数据库
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.views.generic.base import View
from .models import UserProfile
from .forms import LoginForm, RegisterForm
from django.contrib import messages  # Django的信息显示框架用于显示登录提示信息
from django.contrib.auth.decorators import login_required
# from utils.email_send import send_register_email
# Create your views here.


class CustomBackend(ModelBackend):  # 对原装验证方法的重构
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


@login_required(login_url='login')
def index(request):
    # if request.session.test_cookie_worked():
    #     request.session.delete_test_cookie()
    #     message = ''
    # else:
    #     message = '您的浏览器没有接受cookie'
    # 以下是我们自己用session来验证用户是否登录，可行；但我们在登录视图中使用了Django的login函数，它自动生成了session，可以不用在视图中验证
    # 验证session，直接在index.html中用官方的is_authenticated来验证

    # if 'username' in request.session:
    #     username = request.session['username']#用户资料从自制的Session中获得。只能获得用户名一个，因为只存有用户名

    if request.user.is_authenticated:  # 如果函数头前没有加登录装饰器，这个验证有必要存在，但没有也不影响后面的数据取出
        username = request.user.username  # 使用内置的登录函数可以这样获得登录用户的全部数据放到username中
        user = UserProfile.objects.get(username=username)
        # user = UserProfile.objects.get(grade=1)#这里想要验证一下是不是user包含了用户的全部数据
        return render(request, 'index2.html', {'username': user.username})
    else:
        return render(request, 'login2.html')


# class ActiveUserView(View):  # 激活验证函数
#     def get(self, request,active_code):  # active_code是前端传来的验证字符串
#         all_records = EmailVerifyRecord.objects.filter(code=active_code)
#         if all_records:
#             for record in all_records:
#                 email = record.email
#             user = UserProfile.objects.get(email=email)
#             if user:
#                 user.is_active = True
#                 user.save()
#             else:
#                 return render(request, "active_fail.html")
#         return render(request, "login.html")


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm(request.POST)
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():  # 这里让表单验证函数先验证一下表单的格式是否正确，如果正确再开始查询数据库进行下面真正的验证，从而减轻数据库的负担
            user_name = request.POST.get("username", "")
            if UserProfile.objects.get(email=user_name):
                return render(request, "register.html", {"msg": "该邮箱已存在"}, {"register_form": register_form})
            else:
                pass_word = request.POST.get("password", "")  # 注意这里得到的是用户密码的明文，不能直接存到数据库里
                user_profile = UserProfile()
                user_profile.username = user_name
                user_profile.password = make_password(pass_word)  # 调用系统的加密函数对密码进行加密才能保存到数据库
                user_profile.email = user_name
                user_profile.is_active = False
                user_profile.save()
                # send_register_email(user_name,"register")
                return render(request, "login.html", {"register_form": register_form})
        else:
            return render(request, "register.html", {'msg': "验证失败"})


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
                if user.is_active:  # 用于验证此账号是否有效
                    request.session['username'] = user_name
                    request.session['password'] = pass_word  # 将用户名和密码写入session，用于验证
                    login(request, user)
                    messages.add_message(request, messages.SUCCESS, '登陆成功')
                    return render(request, "index2.html", {"username": user_name})
                else:
                    messages.add_message(request,messages.WARNING, '账号尚未启用')
                    return render(request, 'login2.html')
            else:
                # return render(request, "login.html", {'msg': "用户名或密码错误", "login_form": login_form})
                messages.add_message(request, messages.WARNING, '用户名或密码错误')
                return render(request, "login2.html")
        else:  # 表单格式验证失败直接返回
                # return render(request, "login.html", {"login_form":login_form})#如果表单格式验证不通过，
                # 则返回登陆页面并将login_form返回给前端从而显示其错误信息
                messages.add_message(request, messages.WARNING, '输入格式错误')
                return render(request, "login2.html")


@login_required(login_url='login')
def log_out(request):  # 使用删除session的方式实现注销
    logout(request)
    # if 'username' in request.session:
    #     del request.session["username"]  # 删除session
    messages.add_message(request, messages.INFO, '注销成功')
    return render(request, 'login2.html')
    # else:
    #     return render(request, 'login2.html')


#  自定义登陆函数，但要调用系统的登陆函数,可行，但不推荐；推荐用上面的类的方法的重写来实现,但是用重写类的方法的方式无法使用装饰器来限定登录
# def user_login(request):
#     if request.method == "POST":
#         user_name = request.POST.get("username","")
#         pass_word = request.POST.get("password","")
#         user = authenticate(username=user_name,password=pass_word)
#         if user is not None:
#            login(request,user)
#            return render(request,"index.html")
#         else:
#            return render(request, "login.html", {'msg':"用户名或密码错误"})
#     elif request.method =="GET":
#         return render(request,"login.html",{})

# class View
