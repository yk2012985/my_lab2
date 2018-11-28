from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.views.generic.base import View
from .models import Template
from django.contrib.auth.decorators import login_required
# Create your views here.


class ReportView(View):
    def get(self, request):
        mubans = Template.objects.all()
        return render(request, "report.html", {"muban": mubans})
