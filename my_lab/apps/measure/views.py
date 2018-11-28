from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic.base import View
from .models import Laboratory, Device
from .forms import LabForm, DeviceForm
from django.contrib.auth.decorators import login_required

@login_required(login_url='login')
def labs_view(request):
    labs = Laboratory.objects.all()
    return render(request, 'labs.html', {'labs': labs})


@login_required(login_url='login')
def lab_info(request, lab_id):
    lab = Laboratory.objects.get(pk=lab_id)
    devices = Device.objects.all()
    return render(request, 'lab_info.html', {'lab': lab,
                                             'devices': devices
                                             }
                  )


@login_required(login_url='login')
def lab_edit(request, lab_id):  # 此函数承担两个任务，添加课目与修改课目，关键看id是否为0
    if str(lab_id) == '0':
        return render(request, 'lab_edit.html')
    else:
        lab = Laboratory.objects.get(pk=lab_id)
        return render(request, 'lab_edit.html', {'lab': lab})



def lab_edit_action(request):
    lab_form = LabForm(request.POST)#验证表单格式
    if lab_form.is_valid():
        lab_id = request.POST.get('lab_id', '0')  # get方法的第二个参数是默认值
        if lab_id == '0':
            name = request.POST.get('name', '')
            locate = request.POST.get('locate', '')
            admin = request.POST.get('admin', '')
            detail = request.POST.get('detail', '')
            lab = Laboratory(name=name, locate=locate, admin=admin, detail=detail)
            lab.save()
            labs = Laboratory.objects.all()
            return render(request, 'labs.html', {'labs': labs})
        else:
            lab = Laboratory.objects.get(pk=lab_id)
            lab.name = request.POST.get('name', '')
            lab.locate = request.POST.get('locate', '')
            lab.admin = request.POST.get('admin', '')
            lab.detail = request.POST.get('detail', '')
            lab.save()
            return render(request, 'lab_info.html', {'lab': lab,
                                                     }
                          )
    else:
        lab_id = request.POST.get('lab_id', '0')  # get方法的第二个参数是默认值
        lab = Laboratory.objects.get(pk=lab_id)
        return render(request, '.html', {'lab': lab
                                         }
                      )


def lab_delete(request, lab_id):
    lab = Laboratory.objects.get(pk=lab_id)
    lab.delete()
    labs = Laboratory.objects.all()
    return render(request, 'labs.html', {'labs': labs})

