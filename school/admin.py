from django.contrib import admin
from datetime import datetime
from school.models import *
from django.db.models import F, Count
from . import models
from import_export.admin import ImportExportMixin
from django.utils import timezone

# Register your models here.
def change_ngay_gui_bai(modeladmin, request, queryset):
    queryset.update(ngay_gui_bai = timezone.now())
def view_update(modeladmin, request, queryset):
    queryset.update(viewed=F('viewed') + 1)
def si_so_update(modeladmin,request, queryset):
    students = models.Student.objects.values('lop_id', 'lop_id__lop', 'lop_id__ma_khoi').annotate(
        total=Count('lop_id')).order_by('lop_id')
    for i in students:
        queryset.filter(lop_id=i['lop_id']).update(si_so=i['total'])  
            
change_ngay_gui_bai.short_description = "Đánh dấu ngày gửi bài thành hôm nay"
view_update.short_description = "Tăng 1 view"
si_so_update.short_description = "Cập nhật sĩ số của lớp học"

class ResultA(ImportExportMixin, admin.ModelAdmin):
    list_display = ('MaHs','hoc_ky', 'ky_thi', 'lan_thi', 'mon_thi', 'diem_thi')
    list_filter = ('hoc_ky', 'mon_thi', 'ky_thi', )
    
class BlogA(ImportExportMixin, admin.ModelAdmin):
    list_display = ('tieu_de', 'ma_trang_thai', 'ngay_gui_bai','viewed','comments')
    list_filter = ('ngay_gui_bai','viewed','comments', )
    search_fields = ('tieu_de__contains', )
    actions = [change_ngay_gui_bai, view_update]
    
class ClassA(ImportExportMixin, admin.ModelAdmin):
    list_display = ('lop', 'nienkhoa', 'si_so', 'giaovien')
    actions = [si_so_update]
    
class StudentA(ImportExportMixin, admin.ModelAdmin):
    list_display = ('MaHs', 'lop_id', 'name', 'gender')
    list_filter = ('lop_id', 'gender', )
    
class CommentA(admin.ModelAdmin):
    list_filter = ('blog', 'created', )
    
class DocumentA(ImportExportMixin, admin.ModelAdmin):
    list_display = ('ma_khoi', 'ma_mon', 'ten_tai_lieu')
    list_filter = ('ma_khoi', 'ma_mon', 'ten_tai_lieu', )
    
class LikeA(ImportExportMixin, admin.ModelAdmin):
    list_display = ('created', 'blog', 'comment_id', 'islike', 'user')
    list_filter = ('created', 'blog', 'islike',  )
    
admin.site.register(Grade)
admin.site.register(Class, ClassA)
admin.site.register(Student, StudentA)
admin.site.register(NienKhoa)
admin.site.register(Subject)
admin.site.register(Document, DocumentA)
admin.site.register(Library)
admin.site.register(DoanThe)
admin.site.register(BanChuyenTrach)
admin.site.register(ToBoMon)
admin.site.register(Status)
admin.site.register(Category)
admin.site.register(Blog, BlogA)
admin.site.register(City)
admin.site.register(UserProfileInfo)
admin.site.register(Contact)
admin.site.register(Result, ResultA)
admin.site.register(Entrance)
admin.site.register(Admission)
admin.site.register(Comment, CommentA)
admin.site.register(Like, LikeA)

admin.site.site_header = 'PTNK Admin'


