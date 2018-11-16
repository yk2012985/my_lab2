from django import forms
# from captcha.fields import CaptchaField
class LoginForm(forms.Form):
    username = forms.CharField(required=True)  # 这里设置需要验证的表单的内容及格式，
    # 注意这里的两个属性的名称一定要和前端传进来的参数的名称相同，否则无法验证
    password = forms.CharField(required=True,min_length=6)


class RegisterForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=6)
    # captcha = CaptchaField()