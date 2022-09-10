from xml.dom.pulldom import START_DOCUMENT
from django.shortcuts import render
from django.http import JsonResponse
from school.models import Result, Student, Grade, Class, Student
from django.core import serializers
from django.db.models import F, Avg, Case, When, FloatField, Func, Sum, Count
from django.http import HttpResponse
import pandas as pd
import os
import io
from django.conf import settings
from .utils import *
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from . import models
from django.db.models import Count
import pdfkit
from datetime import date
from school.views import * 
grade_list = models.Grade.objects.all()
doanthe_list = models.DoanThe.objects.all()
tobomon_list = models.ToBoMon.objects.all()
banchuyentrach_list = models.BanChuyenTrach.objects.all()
subject_list = models.Subject.objects.all()
now = timezone.now()
latest = models.Blog.objects.latest('pk')
three_newest = models.Blog.objects.order_by('-ngay_gui_bai')[0:3] 

class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 2)'

# Create your views here.
def dashboard_with_pivot(request):
    return render(request, 'report/report.html', {})

def pivot_data(request):
    dataset = Result.objects.all()
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)

def pivot_data2(request):
    dataset = Class.objects.select_related('ma_khoi')
    data = serializers.serialize('json', dataset)
    return JsonResponse(data, safe=False)

def summary(request):
    username = request.session.get('username', 0)
    #Update sĩ số
    students = Student.objects.values('lop_id', 'lop_id__lop', 'lop_id__ma_khoi').annotate(
        total=Count('lop_id')).order_by('lop_id')
    for i in students:
        Class.objects.filter(lop_id=i['lop_id']).update(si_so=i['total'])
    today = date.today()
    d = today.strftime("%d/%m/%Y")
    
    student_list = Class.objects.values('ma_khoi__ten_khoi','lop','si_so').order_by('ma_khoi__ten_khoi', 'lop')
    
    path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
    
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    
    
    html_string = render_to_string(
        'report/summary.html', {'student':student_list, 'day':d, 
                                'latest':latest,
                                'three_newest':three_newest,
                                'username':username})
    pdfkit.from_string(html_string, os.path.join(
        os.path.expanduser('~'), 'Documents', 'summary.pdf'), configuration=config)

    html = "<html><body><h3>Thống kê đã được lưu vào tập tin summary.pdf trong thư mục Documents.</h3></body></html>"
    return HttpResponse(html)

def stats(request):
    username = request.session.get('username', 0)
    #Update sĩ số
    students = Student.objects.values('lop_id', 'lop_id__lop', 'lop_id__ma_khoi').annotate(
        total=Count('lop_id')).order_by('lop_id')
    for i in students:
        Class.objects.filter(lop_id=i['lop_id']).update(si_so=i['total'])
    result_list = Class.objects.all()
    result = pd.DataFrame({'Class': [c.lop for c in result_list], 'Number': [c.si_so for c in result_list]})
    pie = get_pie(result.Number, result.Class, "Thống kê học sinh theo lớp")
    
    si_so_10 = Class.objects.filter(ma_khoi=1).values('si_so').aggregate(si_so=(Sum('si_so')))['si_so']
    si_so_11 = Class.objects.filter(ma_khoi=2).values('si_so').aggregate(si_so=(Sum('si_so')))['si_so']
    si_so_12 = Class.objects.filter(ma_khoi=3).values('si_so').aggregate(si_so=(Sum('si_so')))['si_so']
    total = pd.DataFrame(
        {
        'Grade': ['Khối 10', 'Khối 11', 'Khối 12'],
        'Student': [si_so_10, si_so_11, si_so_12]
        })
    pie2 = get_pie2(total.Student, total.Grade, 'Thống kê học sinh theo khối')

    return render(request, "report/statistic.html", {
                                                'pie':pie,
                                                'pie2':pie2,
                                                'latest':latest,
                                                'three_newest':three_newest,
                                                'username':username
                                                    })