from django import forms
from .models import Device


class LabForm(forms.Form):
    name = forms.CharField(required=True)
    locate = forms.CharField(required=True)
    admin = forms.CharField(required=True)
    detail = forms.CharField(required=True,widget=forms.Textarea)


# class DeviceForm(forms.Form):
#     class Meta:
#         model = Device
#         fields = ['name', 'laboratory', 'kind', 'brand']
#
#     def __init__(self, *args, **kwargs):
#         super(DeviceForm, self).__init__(*args, **kwargs)
#         self.fields['name'].label = '名称'
#         self.fields['laboratory'].label = '所属实验室'
#         self.fields['kind'].label = '仪器种类'
#         self.fields['brand'].label = '品牌'
class DeviceForm(forms.Form):
    name = forms.CharField(required=True)
    kind = forms.CharField(required=True)
    brand = forms.CharField(required=True)
    detail = forms.CharField(required=True, widget=forms.Textarea)

