from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic.base import View
from .models import Class
from django.contrib.auth.decorators import login_required
# Create your views here.


# class TeacherView(View):
#     def get(self,request):
#         banji = Class.objects.all()
#         return render(request,"teacher_index.html",{"banji":banji})

@login_required(login_url='login')
def teacher_index(request):
    banji = Class.objects.all()
    return render(request, 'teacher_index.html', {'banji':banji})


@login_required(login_url='login')
def student_index(request):
        return render(request, 'student_index.html')