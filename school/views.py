import datetime
import re
from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Count, F, Q, Value
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from WebsiteTHPT.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from . import models
from . import forms
import feedparser
import json
from django.db.models import Avg, Case, When, FloatField, Func, Sum
import urllib.request
from django.utils import timezone
from django.http import HttpResponse

grade_list = models.Grade.objects.all()
doanthe_list = models.DoanThe.objects.all()
tobomon_list = models.ToBoMon.objects.all()
banchuyentrach_list = models.BanChuyenTrach.objects.all()
subject_list = models.Subject.objects.all()
now = timezone.now()
latest = models.Blog.objects.latest('pk')
three_newest = models.Blog.objects.order_by('-ngay_gui_bai')[0:3]  
time = datetime.datetime.now() 

class Round(Func):
    function = 'ROUND'
    template='%(function)s(%(expressions)s, 2)'

def index(request):
    global grade_list, doanthe_list, tobomon_list, banchuyentrach_list, subject_list, now, latest, three_newest
    grade_list = models.Grade.objects.all()
    doanthe_list = models.DoanThe.objects.all()
    tobomon_list = models.ToBoMon.objects.all()
    banchuyentrach_list = models.BanChuyenTrach.objects.all()
    subject_list = models.Subject.objects.all()
    now = timezone.now()
    latest = models.Blog.objects.latest('pk')
    three_newest = models.Blog.objects.order_by('-ngay_gui_bai')[0:3]   
    username = request.session.get('username', 0)
    blog_list = models.Blog.objects.order_by("-ngay_gui_bai")
    get_bloglist = models.Blog.objects.values('id')
    for i in get_bloglist:
        total_comments = models.Comment.objects.filter(blog_id=i['id']).count()
        models.Blog.objects.filter(id=i['id']).update(comments=total_comments)
    time = datetime.datetime.now()

    return render(request, "school/index.html", {'latest': latest, 'blog_list': blog_list, 'username': username, 'grades':grade_list, 'subjects':subject_list, 'three_newest':three_newest, 'time':time})

def profile(request):
    time = datetime.datetime.now()
    username = request.session.get('username', 0)
    last_visit = request.session.get('last_visit', 0)
    request.session['last_visit'] = time.strftime('%B %d, %Y %I:%M %p')
    success = False
    user = models.User.objects.get(username=username)
    profile = models.UserProfileInfo.objects.get(user__username=username)
    activites = models.Comment.objects.filter(isuser=True).filter(name=user).order_by("-created")[0:3]
    if request.method == 'POST':
        global user_form, profile_form
        user_form = forms.UpdateUserForm(request.POST)
        profile_form = forms.UpdateUserProfileInfoForm(request.POST)
        if (user_form.is_valid() and profile_form.is_valid() and user_form.cleaned_data['password'] == user_form.cleaned_data['confirm']):
            user.set_password(user_form.cleaned_data['password'])
            user.save()
            models.User.objects.filter(username=username).update(email = user_form.cleaned_data['email'])
            models.UserProfileInfo.objects.filter(user__username=username).update(fullname = profile_form.cleaned_data['fullname'])
            models.UserProfileInfo.objects.filter(user__username=username).update(address = profile_form.cleaned_data['address'])
            models.UserProfileInfo.objects.filter(user__username=username).update(phone = profile_form.cleaned_data['phone'])
            if 'image' in request.FILES:
                profile.image = request.FILES['image']
                profile.save()
                      
        if user_form.cleaned_data['password'] != user_form.cleaned_data['confirm']:
            user_form.add_error('confirm', 'Mật khẩu xác nhận khác mật khẩu') 
        success = True            
    else:
        user_form = forms.UpdateUserForm()
        profile_form = forms.UpdateUserProfileInfoForm()
    
    return render(request, "school/profile.html", {'latest': latest, 'username': username, 'grades':grade_list, 'subjects':subject_list, 'three_newest':three_newest, 'user_form': user_form, 'profile_form': profile_form, 'success': success, 'user':user, 'profile': profile, 'last_visit': last_visit, 'activities':activites})
 
           
def intro(request):
    username = request.session.get('username', 0)
    return render(request, "school/intro.html", {'latest': latest, 'username': username, 'grades':grade_list, 'subjects':subject_list, 'three_newest':three_newest})

def doanthe(request, pk):
    username = request.session.get('username', 0)
    doan_list = []
    ma_doan_the = pk
    if pk != 0:
        doan_list = models.DoanThe.objects.filter(
            ma_doan_the=pk)
    else:
        doan_list = models.DoanThe.objects.all()
    return render(request, "school/doanthe.html", {'today': now,
                   'username': username,
                   'latest':latest,
                   'doanthe': doanthe_list,
                   'doan_list': doan_list,
                   'pk': pk,
                   'three_newest':three_newest
                   })

def doanthe_detail(request, pk):
    username = request.session.get('username', 0)
    doanthe = models.DoanThe.objects.filter(pk=pk)
    return render(request, "school/doanthe-detail.html", {'latest': latest, 'username': username, 'grades':grade_list, 'subjects':subject_list, 'three_newest':three_newest, 'pk': pk, 'doanthe':doanthe})


def tobomon(request, pk):
    username = request.session.get('username', 0)
    to_list = []
    ma_to = pk
    if pk != 0:
        to_list = models.ToBoMon.objects.filter(
            ma_to=pk)
    else:
        to_list = models.ToBoMon.objects.all()
    return render(request, "school/tobomon.html", {'today': now,
                   'username': username,
                   'latest':latest,
                   'tobomon': tobomon_list,
                   'to_list': to_list,
                   'pk': pk,
                   'three_newest':three_newest
                   })
    
def tobomon_detail(request, pk):
    username = request.session.get('username', 0)
    tobomon = models.ToBoMon.objects.filter(pk=pk)
    return render(request, "school/tobomon-detail.html", {'latest': latest, 'username': username, 'grades':grade_list, 'subjects':subject_list, 'three_newest':three_newest, 'pk': pk, 'tobomon':tobomon})


def bct(request, pk):
    username = request.session.get('username', 0)
    bct_list = []
    ma_ban = pk
    if pk != 0:
        bct_list = models.BanChuyenTrach.objects.filter(
            ma_ban=pk)
    else:
        bct_list = models.BanChuyenTrach.objects.all()
    return render(request, "school/bct.html", {'today': now,
                   'username': username,
                   'latest':latest,
                   'banchuyentrach': banchuyentrach_list,
                   'bct_list': bct_list,
                   'pk': pk,
                   'three_newest':three_newest
                   })


def feeds(request):
    news_feed = feedparser.parse("https://www.eschoolnews.com/resource-library/feed/")
    entry = news_feed.entries
    username = request.session.get('username', 0)
    return render(request, "school/feeds.html",
                  {'today': now,
                   'username': username,
                   'feeds': entry,
                   'latest':latest,
                   'three_newest':three_newest
                   })


def result(request):
    profile = []

    hk_list = ['Học kỳ 1', 'Học kỳ 2']
    
    if request.method == 'GET':
        if request.GET.get('id'):
                hk = request.GET.get('id')
        
    username = request.session.get('username', 0)
    if request.method == 'GET':
        if request.GET.get('key'):
                search_str2 = request.GET.get('key')
        else:
            search_str2 = ''

        if search_str2 != '':
            profile = models.Student.objects.filter(MaHs=search_str2)
            try:
                min_toan = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Thường xuyên').filter(mon_thi=1).filter(MaHs = profile[0])
                min_van = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Thường xuyên').filter(mon_thi=2).filter(MaHs = profile[0])
                min_ly = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Thường xuyên').filter(mon_thi=3).filter(MaHs = profile[0])
                min_hoa = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Thường xuyên').filter(mon_thi=4).filter(MaHs = profile[0])
                min_su = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Thường xuyên').filter(mon_thi=5).filter(MaHs = profile[0])
                min_dia = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Thường xuyên').filter(mon_thi=6).filter(MaHs = profile[0])
                min_tin = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Thường xuyên').filter(mon_thi=7).filter(MaHs = profile[0])
                min_nn = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Thường xuyên').filter(mon_thi=8).filter(MaHs = profile[0])
                min_sinh = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Thường xuyên').filter(mon_thi=9).filter(MaHs = profile[0])
                          
                mid_toan = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Giữa kỳ').filter(mon_thi=1).filter(MaHs = profile[0])
                mid_van = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Giữa kỳ').filter(mon_thi=2).filter(MaHs = profile[0])
                mid_ly = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Giữa kỳ').filter(mon_thi=3).filter(MaHs = profile[0])
                mid_hoa = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Giữa kỳ').filter(mon_thi=4).filter(MaHs = profile[0])
                mid_su = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Giữa kỳ').filter(mon_thi=5).filter(MaHs = profile[0])
                mid_dia = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Giữa kỳ').filter(mon_thi=6).filter(MaHs = profile[0])
                mid_tin = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Giữa kỳ').filter(mon_thi=7).filter(MaHs = profile[0])
                mid_nn = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Giữa kỳ').filter(mon_thi=8).filter(MaHs = profile[0])
                mid_sinh = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Giữa kỳ').filter(mon_thi=9).filter(MaHs = profile[0])
                
                fin_toan = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Cuối kỳ').filter(mon_thi=1).filter(MaHs = profile[0])
                fin_van = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Cuối kỳ').filter(mon_thi=2).filter(MaHs = profile[0])
                fin_ly = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Cuối kỳ').filter(mon_thi=3).filter(MaHs = profile[0])
                fin_hoa = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Cuối kỳ').filter(mon_thi=4).filter(MaHs = profile[0])
                fin_su = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Cuối kỳt').filter(mon_thi=5).filter(MaHs = profile[0])
                fin_dia = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Cuối kỳ').filter(mon_thi=6).filter(MaHs = profile[0])
                fin_tin = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Cuối kỳ').filter(mon_thi=7).filter(MaHs = profile[0])
                fin_nn = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Cuối kỳ').filter(mon_thi=8).filter(MaHs = profile[0])
                fin_sinh = models.Result.objects.filter(hoc_ky=hk).filter(ky_thi='Cuối kỳ').filter(mon_thi=9).filter(MaHs = profile[0])
                        
                    
                class Average1(Func):
                    function = len(min_toan) + len(mid_toan)*2 + len(fin_toan)*3
                    template='%(expressions)s/%(function)s' 
                    
                class Average2(Func):
                    function = len(min_van) + len(mid_van)*2 + len(fin_van)*3
                    template='%(expressions)s/%(function)s' 
                    
                class Average3(Func):
                    function = len(min_ly) + len(mid_ly)*2 + len(fin_ly)*3
                    template='%(expressions)s/%(function)s' 
                    
                    
                class Average4(Func):
                    function = len(min_hoa) + len(mid_hoa)*2 + len(fin_hoa)*3
                    template='%(expressions)s/%(function)s' 
                    
                    
                class Average5(Func):
                    function = len(min_su) + len(mid_su)*2 + len(fin_su)*3
                    template='%(expressions)s/%(function)s' 
                    
                class Average6(Func):
                    function = len(min_dia) + len(mid_dia)*2 + len(fin_dia)*3
                    template='%(expressions)s/%(function)s' 
                    
                    
                class Average7(Func):
                    function = len(min_tin) + len(mid_tin)*2 + len(fin_tin)*3
                    template='%(expressions)s/%(function)s' 
                    
                    
                class Average8(Func):
                    function = len(min_nn) + len(mid_nn)*2 + len(fin_nn)*3
                    template='%(expressions)s/%(function)s' 
                    
                class Average9(Func):
                    function = len(min_sinh) + len(mid_sinh)*2 + len(fin_sinh)*3
                    template='%(expressions)s/%(function)s' 
                                                                                                             
                    
                tb_toan = models.Result.objects.filter(hoc_ky=hk).filter(mon_thi=1).filter(MaHs = profile[0]).values('diem_thi').aggregate(toan=Round(Average1(Sum(Case(When(ky_thi='Thường xuyên', then=F('diem_thi')),When(ky_thi='Giữa kỳ', then=F('diem_thi')*2),When(ky_thi='Cuối kỳ', then=F('diem_thi')*3))))))['toan']
                tb_van = models.Result.objects.filter(hoc_ky=hk).filter(mon_thi=2).filter(MaHs = profile[0]).values('diem_thi').aggregate(van=Round(Average2(Sum(Case(When(ky_thi='Thường xuyên', then=F('diem_thi')),When(ky_thi='Giữa kỳ', then=F('diem_thi')*2),When(ky_thi='Cuối kỳ', then=F('diem_thi')*3))))))['van']
                tb_ly = models.Result.objects.filter(hoc_ky=hk).filter(mon_thi=3).filter(MaHs = profile[0]).values('diem_thi').aggregate(ly=Round(Average3(Sum(Case(When(ky_thi='Thường xuyên', then=F('diem_thi')),When(ky_thi='Giữa kỳ', then=F('diem_thi')*2),When(ky_thi='Cuối kỳ', then=F('diem_thi')*3))))))['ly']
                tb_hoa = models.Result.objects.filter(hoc_ky=hk).filter(mon_thi=4).filter(MaHs = profile[0]).values('diem_thi').aggregate(hoa=Round(Average4(Sum(Case(When(ky_thi='Thường xuyên', then=F('diem_thi')),When(ky_thi='Giữa kỳ', then=F('diem_thi')*2),When(ky_thi='Cuối kỳ', then=F('diem_thi')*3))))))['hoa']
                tb_su = models.Result.objects.filter(hoc_ky=hk).filter(mon_thi=5).filter(MaHs = profile[0]).values('diem_thi').aggregate(su=Round(Average5(Sum(Case(When(ky_thi='Thường xuyên', then=F('diem_thi')),When(ky_thi='Giữa kỳ', then=F('diem_thi')*2),When(ky_thi='Cuối kỳ', then=F('diem_thi')*3))))))['su']
                tb_dia =  models.Result.objects.filter(hoc_ky=hk).filter(mon_thi=6).filter(MaHs = profile[0]).values('diem_thi').aggregate(dia=Round(Average6(Sum(Case(When(ky_thi='Thường xuyên', then=F('diem_thi')),When(ky_thi='Giữa kỳ', then=F('diem_thi')*2),When(ky_thi='Cuối kỳ', then=F('diem_thi')*3))))))['dia']
                tb_tin = models.Result.objects.filter(hoc_ky=hk).filter(mon_thi=7).filter(MaHs = profile[0]).values('diem_thi').aggregate(tin=Round(Average7(Sum(Case(When(ky_thi='Thường xuyên', then=F('diem_thi')),When(ky_thi='Giữa kỳ', then=F('diem_thi')*2),When(ky_thi='Cuối kỳ', then=F('diem_thi')*3))))))['tin']
                tb_nn = models.Result.objects.filter(hoc_ky=hk).filter(mon_thi=8).filter(MaHs = profile[0]).values('diem_thi').aggregate(nn=Round(Average8(Sum(Case(When(ky_thi='Thường xuyên', then=F('diem_thi')),When(ky_thi='Giữa kỳ', then=F('diem_thi')*2),When(ky_thi='Cuối kỳ', then=F('diem_thi')*3))))))['nn'] 
                tb_sinh = models.Result.objects.filter(hoc_ky=hk).filter(mon_thi=9).filter(MaHs = profile[0]).values('diem_thi').aggregate(sinh=Round(Average9(Sum(Case(When(ky_thi='Thường xuyên', then=F('diem_thi')),When(ky_thi='Giữa kỳ', then=F('diem_thi')*2),When(ky_thi='Cuối kỳ', then=F('diem_thi')*3))))))['sinh']           
            
                tb_list = []
                #Kiểm tra nếu list rỗng
                if tb_toan:
                    tb_list.append(tb_toan)
                if tb_van:
                    tb_list.append(tb_van)
                if tb_ly:
                    tb_list.append(tb_ly)
                if tb_hoa:
                    tb_list.append(tb_hoa)
                if tb_su:
                    tb_list.append(tb_su)
                if tb_dia:
                    tb_list.append(tb_dia)
                if tb_tin:
                    tb_list.append(tb_tin)
                if tb_nn:
                    tb_list.append(tb_nn)
                if tb_sinh:
                    tb_list.append(tb_sinh)
                    
                    
                try:
                    tb_mon = round(sum(tb_list)/len(tb_list),1)
                    
                except:
                    tb_mon = ''  
                    
                try:
                    if tb_mon >= 8 and tb_toan >=6.5 and tb_van>=6.5 and tb_ly >=6.5 and tb_hoa >=6.5 and tb_su >=6.5 and tb_dia>=6.5 and tb_tin >=6.5 and tb_nn >=6.5 and tb_sinh >=6.5 and (tb_toan >= 8 or tb_van >=8):
                            xep_loai = 'Giỏi'
                    elif tb_mon >= 6.5 and tb_toan >=5 and tb_van>=5 and tb_ly >=5 and tb_hoa >=5 and tb_su >=5 and tb_dia>=5 and tb_tin >=5 and tb_nn >=5 and tb_sinh >=5 and (tb_toan >= 6.5 or tb_van >=6.5):
                        xep_loai = 'Khá'
                    elif tb_mon >= 5 and (tb_toan >= 5 or tb_van >=5):
                        xep_loai = 'Trung bình'
                    elif tb_mon >= 3.5 and tb_toan >=2 and tb_van>=2 and tb_ly >=2 and tb_hoa >=2 and tb_su >=2 and tb_dia>=2 and tb_tin >=2 and tb_nn >=2 and tb_sinh >=2:
                        xep_loai = 'Yếu'
                    else:
                        xep_loai = 'Kém'
                except:
                    xep_loai =''
                                             
                return render(request, "school/result.html", {
                                            'latest':latest, 
                                            'username': username,
                                            'search_str2':search_str2, 
                                            'three_newest':three_newest, 
                                            'profile':profile,
                                            
                                            'min_toan': min_toan,
                                            'min_van': min_van,
                                            'min_ly': min_ly,
                                            'min_hoa': min_hoa,
                                            'min_su': min_su,
                                            'min_dia': min_dia,
                                            'min_tin': min_tin,
                                            'min_nn': min_nn,
                                            'min_sinh': min_sinh,
                                            
                                            'mid_toan': mid_toan,
                                            'mid_van': mid_van,
                                            'mid_ly': mid_ly,
                                            'mid_hoa': mid_hoa,
                                            'mid_su': mid_su,
                                            'mid_dia': mid_dia,
                                            'mid_tin': mid_tin,
                                            'mid_nn': mid_nn,
                                            'mid_sinh': mid_sinh,
                                            
                                            'fin_toan': fin_toan,
                                            'fin_van': fin_van,
                                            'fin_ly': fin_ly,
                                            'fin_hoa': fin_hoa,
                                            'fin_su': fin_su,
                                            'fin_dia': fin_dia,
                                            'fin_tin': fin_tin,
                                            'fin_nn': fin_nn, 
                                            'fin_sinh': fin_sinh,                                          
                                            
                                            'hk_list': hk_list,
                                            'hk': hk,
                                            
                                            'tb_toan': tb_toan,
                                            'tb_van': tb_van,
                                            'tb_ly': tb_ly,
                                            'tb_hoa': tb_hoa,
                                            'tb_su': tb_su,
                                            'tb_dia': tb_dia,
                                            'tb_tin': tb_tin,
                                            'tb_nn': tb_nn,
                                            'tb_sinh':tb_sinh,
                                            
                                            'tb_mon': tb_mon,
                                            'xep_loai': xep_loai
                                            })

            except Exception as e:
                return render(request, "school/result.html", {
                                                'latest':latest, 
                                                'username': username,
                                                'search_str2':search_str2, 
                                                'three_newest':three_newest, 
                                                'profile':profile,  'hk_list': hk_list})
                    
    return render(request, "school/result.html", {
                                                'latest':latest, 
                                                'username': username,
                                                'search_str2':search_str2, 
                                                'three_newest':three_newest, 
                                                'profile':profile,  'hk_list': hk_list
                                           
                                                })

def entrance_score(request):
    score = []   
    username = request.session.get('username', 0)
    if request.method == 'GET':
        if request.GET.get('key'):
                search_str2 = request.GET.get('key')
        else:
            search_str2 = ''

        if search_str2 != '':
            score = models.Entrance.objects.filter(SBD=search_str2)
            
    return render(request, "school/entrance-score.html", {
                                                'latest':latest, 
                                                'username': username,
                                                'search_str2':search_str2, 
                                                'three_newest':three_newest, 
                                                'score':score
                                                })

def document(request, pk):
    doc_list = []
    ma_khoi = pk
    username = request.session.get('username', 0)
    if pk != 0:
        doc_list = models.Document.objects.filter(
            ma_khoi=pk).order_by("-ngay_upload")
    else:
        doc_list = models.Document.objects.order_by("-ngay_upload")
        
        
    page = request.GET.get('page', 1)  
    paginator = Paginator(doc_list, 3) 

    try:
        documents = paginator.page(page)
    except PageNotAnInteger:
        documents = paginator.page(1)
    except EmptyPage:
        documents = paginator.page(paginator.num_pages)
        
    return render(request, "school/document.html", {'latest': latest, 'username': username, 'grades':grade_list, 'subjects':subject_list,'doc_list':doc_list, 'documents':documents, 'pk':pk, 'three_newest':three_newest})


def info(request, pk):
    #Update sĩ số
    students = models.Student.objects.values('lop_id', 'lop_id__lop', 'lop_id__ma_khoi').annotate(
        total=Count('lop_id')).order_by('lop_id')
    for i in students:
        models.Class.objects.filter(lop_id=i['lop_id']).update(si_so=i['total'])      
    class_list = []
    ma_khoi = pk
    username = request.session.get('username', 0)
    
    if pk != 0:
        class_list = models.Class.objects.filter(
            ma_khoi=pk).order_by("lop")
    else:
        class_list = models.Class.objects.order_by("lop")
        
        
    page = request.GET.get('page', 1)  
    paginator = Paginator(class_list, 3)

    try:
        classes = paginator.page(page)
    except PageNotAnInteger:
        classes = paginator.page(1)
    except EmptyPage:
        classes = paginator.page(paginator.num_pages)
  
    return render(request, "school/info.html", {'latest': latest, 'username': username, 'grades':grade_list, 'subjects':subject_list,'class_list':class_list, 'classes':classes, 'pk':pk, 'three_newest':three_newest})

def info_detail(request, pk):
    username = request.session.get('username', 0)
    class_select = models.Class.objects.filter(pk=pk)
    students = models.Student.objects.filter(lop_id=pk).order_by('MaHs')
   
    return render(request, "school/info-detail.html",
                  {'today': now,
                   'students':students,
                   'latest': latest,
                   'username': username, 
                   'grades':grade_list,
                   'pk':pk,
                   'three_newest':three_newest,
                   'class':class_select
                   })
    
def entrance(request):
    username = request.session.get('username', 0)
    result =''
    form = forms.FormAdmission()
    if request.method == 'POST':
        form = forms.FormAdmission(request.POST, models.Admission)
        if form.is_valid():
            result = "Form hợp lệ"
            request.POST._mutable = True
            post = form.save(commit=False)
            post.name = form.cleaned_data['name']
            post.phone_number = form.cleaned_data['phone_number']
            post.email = form.cleaned_data['email']
            post.password = form.cleaned_data['school']
            post.password = form.cleaned_data['classroom']
            post.save()
            result = "Chúng tôi đã nhận thông tin và sẽ phản hồi sớm."
            email_address = form.cleaned_data['email']
            content_1 = form.cleaned_data['school']
            content_2 = form.cleaned_data['classroom']
            subject = 'Tuyển sinh vào trường PTNK.'
            message = 'Chúng tôi đã nhận thông tin và sẽ phản hồi sớm.<br/> Cảm ơn bạn.'
            recepient = str(email_address)
            html_content = '<h3 style="color:blue"><i>Xin chào bạn</i></h3>'\
             + '<strong>Thông tin thí sinh: </strong>'\
             + '<h5><strong>Họ và Tên: </strong>' + form.cleaned_data['name'] +'</h5>'\
             + '<h5><strong>Trường: </strong>' + content_1 +'</h5>'\
             + '<h5><strong>Lớp: </strong>' + content_2 +'</h5>'\
             + '<h4 style="color:red">' + message + '</h4>'
            msg = EmailMultiAlternatives(subject, message, EMAIL_HOST_USER, [recepient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
    else:
        form = forms.FormAdmission()
   
    return render(request, "school/entrance.html", {'form':form, 'result': result, 'latest': latest, 'username': username, 'grades':grade_list, 'subjects':subject_list, 'three_newest':three_newest})

def contact(request):
    username = request.session.get('username', 0)
    result =''
    form = forms.FormContact()
    if request.method == 'POST':
        form = forms.FormContact(request.POST, models.Contact)
        if form.is_valid():
            result = "Form hợp lệ"
            request.POST._mutable = True
            post = form.save(commit=False)
            post.name = form.cleaned_data['name']
            post.phone_number = form.cleaned_data['phone_number']
            post.email = form.cleaned_data['email']
            post.password = form.cleaned_data['subject']
            post.password = form.cleaned_data['message']
            post.save()
            result = "Chúng tôi đã nhận thông tin và sẽ phản hồi sớm."
            email_address = form.cleaned_data['email']
            content = form.cleaned_data['message']
            subject = 'Liên hệ với Trường PTNK.'
            message = 'Chúng tôi đã nhận thông tin và sẽ phản hồi sớm.<br/> Cảm ơn bạn.'
            recepient = str(email_address)
            html_content = '<h3 style="color:blue"><i>Xin chào '+ form.cleaned_data['name'] +',</i></h3>'\
             + '<strong>Nội dung: </strong>'\
             + content\
             + '<h4 style="color:red">' + message + '</h4>'
            msg = EmailMultiAlternatives(subject, message, EMAIL_HOST_USER, [recepient])
            msg.attach_alternative(html_content, "text/html")
            msg.send()
    else:
        form = forms.FormContact()
   
    return render(request, "school/contact.html", {'form':form,'result':result, 'latest': latest, 'username': username, 'grades':grade_list, 'three_newest':three_newest})

def blog(request, pk):
    get_bloglist = models.Blog.objects.values('id')
    for i in get_bloglist:
        total_comments = models.Comment.objects.filter(blog_id=i['id']).count()
        models.Blog.objects.filter(id=i['id']).update(comments=total_comments)
    username = request.session.get('username', 0)
    blog_select = models.Blog.objects.get(pk = pk)
    blog_list = models.Blog.objects.order_by("-ngay_gui_bai")
    page = request.GET.get('page', 1) 
    paginator = Paginator(blog_list, 3)

    try:
        blog_page = paginator.page(page)
    except PageNotAnInteger:
        blog_page = paginator.page(1)
    except EmptyPage:
        blog_page = paginator.page(paginator.num_pages)
   
    return render(request, "school/blog.html",
                 { 'today': now,
                   'blog':blog_select,
                   'latest': latest,
                   'username': username,
                   'grades':grade_list,
                   'blog_page':blog_page,
                   'blog_list': blog_list,
                   'pk':pk,
                   'three_newest':three_newest
                 })

def blog_detail(request, pk):
    get_bloglist = models.Blog.objects.values('id')
    for i in get_bloglist:
        total_comments = models.Comment.objects.filter(blog_id=i['id']).count()
        models.Blog.objects.filter(id=i['id']).update(comments=total_comments)
    username = request.session.get('username', 0)
    blog_select = models.Blog.objects.get(pk = pk)
    comments = models.Comment.objects.filter(blog = blog_select).order_by("-created")
    blogs = models.Blog.objects.filter(pk=pk)
    models.Blog.objects.filter(pk=blog_select.pk).update(viewed=F('viewed') + 1)
    blog_select.refresh_from_db()
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if username:
            user = models.User.objects.get(username=username)
            user_profile = models.UserProfileInfo.objects.get(user=user)
            if form.is_valid():
                Comment = models.Comment(name = username, email=form.cleaned_data['email'],
                content=form.cleaned_data['content'], avatar=user_profile.image,
                blog=blog_select, isuser=True)
                Comment.save()
        else:
            if form.is_valid():
                Comment = models.Comment(name = form.cleaned_data['name'], email=form.cleaned_data['email'],
                content=form.cleaned_data['content'],
                blog=blog_select)
                Comment.save()        
    else:
        form = forms.CommentForm()
        
    # Kiểm tra nếu đã like hoặc dislike
    if username:
        likes_list = models.Like.objects.filter(blog=blog_select, user=request.user).values('comment_id', 'islike')
        get_not_likes_list = models.Comment.objects.filter(blog=blog_select).values('id')
        not_likes_list = []
        for i in get_not_likes_list:
            not_likes_list.append(i['id'])
        for k in likes_list:
            not_likes_list.remove(k['comment_id'])
    else:
        likes_list = ''
        not_likes_list = ''
        
    # Update số like cho mỗi comment   
    likes = models.Like.objects.filter(islike=True).values('comment_id').annotate(
        total=Count('comment_id')).order_by('comment_id')
    for i in likes:
        like_track = models.Comment.objects.filter(id=i['comment_id']).update(total_likes=i['total'])   
        
    dislikes = models.Like.objects.filter(islike=False).values('comment_id').annotate(
        total=Count('comment_id')).order_by('comment_id')
    for i in dislikes:
        dislike_track = models.Comment.objects.filter(id=i['comment_id']).update(total_dislikes=i['total'])  
    
    if request.method == 'POST':
        if request.POST.get('u') is not None:
            checkpoint = models.Like.objects.filter(user = request.user, 
                                                        blog = blog_select, comment_id=request.POST.get('u'), islike=True).count()
            if checkpoint == 0:
                models.Like.objects.get_or_create(user = request.user, 
                                                    blog = blog_select, comment_id=request.POST.get('u'), islike=True)
                
                if models.Like.objects.filter(user = request.user, 
                                                        blog = blog_select, comment_id=request.POST.get('u'), islike=False).count() > 0:
                    models.Like.objects.filter(user = request.user, 
                                                        blog = blog_select, comment_id=request.POST.get('u'), islike=False).delete()
                    models.Comment.objects.filter(id=request.POST.get('u')).update(total_dislikes=dislike_track-1)  
                    
            elif checkpoint > 0:
                models.Like.objects.filter(user = request.user, 
                                                    blog = blog_select, comment_id=request.POST.get('u'), islike=True).delete()
                models.Comment.objects.filter(id=request.POST.get('u')).update(total_likes=like_track-1)   
                
         
        if request.POST.get('d') is not None:
            checkpoint_2 = models.Like.objects.filter(user = request.user, 
                                                    blog = blog_select, comment_id=request.POST.get('d'), islike=False).count()
            if checkpoint_2 == 0:
                models.Like.objects.get_or_create(user = request.user, 
                                                    blog = blog_select, comment_id=request.POST.get('d'), islike=False)
                
                if models.Like.objects.filter(user = request.user, 
                                                        blog = blog_select, comment_id=request.POST.get('d'), islike=True).count() > 0:           
                    models.Like.objects.filter(user = request.user, 
                                                        blog = blog_select, comment_id=request.POST.get('d'), islike=True).delete()
                    models.Comment.objects.filter(id=request.POST.get('d')).update(total_likes=like_track-1)  
                     
            elif checkpoint_2 > 0:
                models.Like.objects.filter(user = request.user, 
                                                    blog = blog_select, comment_id=request.POST.get('d'), islike=False).delete()
                models.Comment.objects.filter(id=request.POST.get('d')).update(total_dislikes=dislike_track-1)   
                
        return redirect("school:blog-detail.html", pk=pk)

                
    page = request.GET.get('page', 1) 
    paginator = Paginator(comments, 4)

    try:
        com = paginator.page(page)
    except PageNotAnInteger:
        com = paginator.page(1)
    except EmptyPage:
        com = paginator.page(paginator.num_pages)
    
    return render(request, "school/blog-detail.html",
                  {'today': now,
                   'blog':blog_select,
                   'blogs':blogs,
                   'latest': latest,
                   'username': username, 
                   'grades':grade_list,
                   'pk':pk,
                   'three_newest':three_newest,
                   'form':form,
                   'comments':comments,
                   'com':com,
                   'likes_list': likes_list,
                   'not_likes_list': not_likes_list
                   })

def library(request):
    username = request.session.get('username', 0)
    return render(request, "school/library.html", {'latest': latest, 'username':username, 'grades':grade_list, 'three_newest':three_newest})

def search(request):
    global search_str
    username = request.session.get('username', 0)
    get_bloglist = models.Blog.objects.values('id')
    for i in get_bloglist:
        total_comments = models.Comment.objects.filter(blog_id=i['id']).count()
        models.Blog.objects.filter(id=i['id']).update(comments=total_comments)
    blogs = []
    docs = []
    if request.method == 'GET':
        
        if request.GET.get('key'):
            search_str = request.GET.get('key')
        else:
            search_str = ''
        
        if search_str != '':
            blogs = models.Blog.objects.filter(Q(tieu_de__contains=search_str) | Q(noi_dung__contains=search_str)).order_by("-ngay_gui_bai")
            
        if request.GET.get('key'):
                search_str = request.GET.get('key')
        else:
            search_str = ''
        
        if search_str != '':
            docs = models.Document.objects.filter(Q(ten_tai_lieu__contains=search_str) | Q(tom_tat__contains=search_str)).order_by("-ngay_upload")
    for blog in blogs:
        blog.noi_dung= re.sub('<[^<]+?', '', blog.noi_dung)
    for doc in docs:
        doc.tom_tat= re.sub('<[^<]+?', '', doc.tom_tat)
    numbers = len(blogs)
    numbers2 = len(docs)
    
    return render(request, "school/search.html", {'today':now,'latest':latest,'blogs':blogs,'docs':docs, 'numbers':numbers, 'numbers2':numbers2,'search_str':search_str, 'username': username, 'grades':grade_list, 'three_newest':three_newest})


def register(request):
    registered = False
    if request.method == "POST":
         form_user = forms.UserForm(data=request.POST)       
         form_por = forms.UserProfileInfoForm(data=request.POST) 
         if (form_user.is_valid() and form_por.is_valid() and form_user.cleaned_data['password'] == form_user.cleaned_data['confirm']):
             user = form_user.save()   
             user.set_password(user.password)         
             user.save()     
             
             profile = form_por.save(commit=False)
             profile.user = user
             if 'image' in request.FILES:
                 profile.image = request.FILES['image']
             profile.save()
             
             registered = True
             
             #EMAIL
             email_address = form_user.cleaned_data['email']
             subject = 'Tài khoản của bạn đã được tạo.'
             message = 'Xem thông tin tuyển sinh và tra cứu điểm thi tại: https://ptnk.herokuapp.com/entrance-score/.<br/> Cám ơn.'
             recepient = str(email_address)
             html_content = '<h2 style="color:blue"><i>Xin chào '+ form_user.cleaned_data['username'] +',</i></h2>'\
             + '<p>Xem nhiều nội dung hơn tại <strong>Website PTNK</strong>.</p>'\
             + '<h4 style="color:red">' + message + '</h4>'
             msg = EmailMultiAlternatives(subject, message, EMAIL_HOST_USER, [recepient])
             msg.attach_alternative(html_content, "text/html")
             msg.send()
         if form_user.cleaned_data['password'] != form_user.cleaned_data['confirm']:
             form_user.add_error('confirm', 'Mật khẩu xác nhận khác mật khẩu')
             print(form_user.errors, form_por.errors)
    else:
        form_user = forms.UserForm()
        form_por = forms.UserProfileInfoForm()   
        
    username = request.session.get('username', 0)
    return render(request, 'school/register.html',
                  {'form_user':form_user,
                  'form_por':form_por,
                  'registered': registered,
                  'username': username,
                  'latest': latest,
                  'grades':grade_list,
                  'three_newest':three_newest
                  })
    
def log_in(request):
    username = request.session.get('username', 0)
    login_result = 0
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            request.session['username'] = username
            username = request.session.get('username', 0)
            login_result = 1
            return render(request, "school/login.html",{'login_result': login_result, 'latest':latest, 'grades':grade_list, 'three_newest':three_newest, 'username': username})
        else:
            print("Bạn không thể đăng nhập.")
            print("Tên đăng nhập: {} và mật khẩu: {}".format(username,password))
            login_result = 2
            return render(request, "school/login.html", {'login_result': login_result, 'latest':latest, 'grades':grade_list, 'three_newest':three_newest})
    else:
        return render(request, "school/login.html", {'latest':latest, 'grades':grade_list, 'three_newest':three_newest})
    
@login_required
def log_out(request):
    logout(request)
    return redirect("school:index.html")




