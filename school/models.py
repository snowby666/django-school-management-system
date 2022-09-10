from ast import Sub
from django.db import models
import datetime
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone

# Create your models here.
class Status(models.Model):
    ma_trang_thai = models.AutoField(primary_key=True)
    trang_thai = models.CharField(max_length=100)
    def __str__(self):
        return self.trang_thai
    
class Grade(models.Model):
    ma_khoi = models.AutoField(primary_key=True)
    ten_khoi = models.CharField(max_length=100)
    khoi_tit = models.CharField(max_length=200, null=True)
    def __str__(self):
        return self.ten_khoi
    
class NienKhoa(models.Model):
    
    nien_khoa = models.CharField(max_length=20)
    tit = models.CharField(max_length=200)

    def __str__(self):
        return self.nien_khoa
    
class Class(models.Model):
    ma_khoi = models.ForeignKey(Grade, max_length=3, on_delete=models.PROTECT)
    lop_id = models.AutoField(primary_key=True)
    nienkhoa = models.ForeignKey(NienKhoa, max_length=20, on_delete=models.PROTECT)
    lop = models.CharField(max_length=10, null=True)
    ma_lop = models.CharField(max_length=10, null=True)
    si_so = models.IntegerField(null=True)
    giaovien = models.TextField(null = True)

    def __str__(self):
        return self.lop



class Student(models.Model):
    lop_id = models.ForeignKey(Class, on_delete=models.CASCADE)
    MaHs = models.CharField(max_length=11, unique=True)
    name = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=10, null=True,
        choices=[
            ('Nam','Nam'),
            ('Nữ', 'Nữ')
        ])
    phone_number = models.CharField(max_length=100, null=True)
    address = models.CharField(max_length=200, unique=False, null=True)
    hinh = models.ImageField(upload_to="school/images",
                              default="school/images/default.png", null=True)
    ho_ten_cha = models.CharField(max_length=100, null=True)
    ho_ten_me = models.CharField(max_length=100, null=True)
    
    def __str__(self):
        return self.MaHs
    
      
    
class Subject(models.Model):
    ma_mon = models.AutoField(primary_key=True)
    ten_mon = models.CharField(max_length=100)
    monhoc_tit = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.ten_mon

    
class Result(models.Model):
    MaHs = models.ForeignKey(Student, on_delete=models.CASCADE)
    hoc_ky = models.CharField(max_length=10, null=True,
        choices=[
            ('Học kỳ 1','Học kỳ 1'),
            ('Học kỳ 2', 'Học kỳ 2'),
        ])
    ky_thi = models.CharField(max_length=20, null=True,
        choices=[
            ('Thường xuyên','Thường xuyên'),
            ('Giữa kỳ','Giữa kỳ'),
            ('Cuối kỳ','Cuối kỳ'),
        ])
    mon_thi = models.ForeignKey(Subject, on_delete=models.CASCADE)
    lan_thi = models.IntegerField(null=True,  
        choices=[
            (1,'1'),
            (2,'2'),
            (3,'3'),
        ])
    diem_thi = models.FloatField(null=True)
    ngay_thi = models.DateField(null=True)
    
    def __str__(self):
        return '{}'.format(self.MaHs)
    
class Entrance(models.Model):
    SBD = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100, null=True)
    toan = models.FloatField(blank=True, null=True)    
    van = models.FloatField(blank=True, null=True)
    ly = models.FloatField(blank=True, null=True)    
    hoa = models.FloatField(blank=True, null=True)
    su = models.FloatField(blank=True, null=True)    
    dia = models.FloatField(blank=True, null=True)
    tin = models.FloatField(blank=True, null=True)    
    nn = models.FloatField(blank=True, null=True)
    sinh = models.FloatField(blank=True, null=True)
    
    def __str__(self):
        return self.SBD
    
class Library(models.Model):
    ma_thu_vien = models.AutoField(primary_key=True)
    ten_thu_vien = models.CharField(max_length=100)
    thuvien_tit = models.CharField(max_length=200, null=True)
    ten_full = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.ten_thu_vien
    
class Document(models.Model):
    doc_id = models.AutoField(primary_key=True)
    ma_thu_vien = models.ForeignKey(Library, on_delete=models.CASCADE)
    ma_mon = models.ForeignKey(Subject, null=True, on_delete=models.CASCADE)
    ma_khoi = models.ForeignKey(Grade, null=True, on_delete=models.CASCADE)
    ma_trang_thai = models.ForeignKey(Status, on_delete=models.CASCADE)
    ten_tai_lieu = models.CharField(max_length=200)
    tit = models.CharField(max_length=200, null=True)
    tom_tat = models.TextField()
    pdf = models.CharField(max_length=200, null=True)
    pdf_size = models.IntegerField(null=True)
    file_goc = models.CharField(max_length=200, null=True)
    file_goc_size = models.IntegerField(null=True)
    ngay_upload = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.ten_tai_lieu
    
class Category(models.Model):
    ma_muc = models.AutoField(primary_key=True)
    ten_muc = models.CharField(max_length=200)
    hinh = models.ImageField(upload_to="school/images",
                              default="school/images/default.png", null=True)
    mo_ta = models.TextField()
    
    def __str__(self):
        return self.ten_muc
    
class Blog(models.Model):
    ma_muc = models.ForeignKey(Category, on_delete=models.CASCADE)
    ma_tieu_muc = models.IntegerField(null=True)
    ma_trang_thai = models.ForeignKey(Status, on_delete=models.CASCADE)
    tieu_de = models.CharField(max_length=200)
    tit = models.CharField(max_length=200, null=True)
    tom_tat = models.TextField()
    noi_dung = RichTextUploadingField(blank=True, null=True)
    ngay_gui_bai = models.DateTimeField(default=timezone.now)
    ngay_xuat_ban = models.DateTimeField(default=timezone.now)
    ngay_het_han = models.DateTimeField(default=timezone.now)
    hinh = models.ImageField(upload_to="school/images",
                              default="school/images/default.png", null=True)
    nguon = models.CharField(max_length=200, null=True)
    nguoi_gui = models.CharField(max_length=200,  null=True)
    viewed = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    
    def __str__(self):
        return self.tieu_de
    
class BanChuyenTrach(models.Model):
    ma_ban = models.AutoField(primary_key=True)
    ten_ban = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    mo_ta = RichTextUploadingField()
    hinh = models.ImageField(upload_to="school/images",
                              default="school/images/default.png", null=True)
    
    def __str__(self):
        return self.ten_ban
    
class DoanThe(models.Model):
    ma_doan_the = models.AutoField(primary_key=True)
    ten_doan_the = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    mo_ta = RichTextUploadingField()
    hinh = models.ImageField(upload_to="school/images",
                              default="school/images/default.png", null=True)
    
    def __str__(self):
        return self.ten_doan_the

class ToBoMon(models.Model):
    ma_to = models.AutoField(primary_key=True)
    ma_muc = models.ForeignKey(Category, null=True, on_delete=models.CASCADE)
    ten_to = models.CharField(max_length=200)
    tit = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)
    mo_ta = RichTextUploadingField()
    gioithieu = RichTextUploadingField(default='')
    hinh = models.ImageField(upload_to="school/images",
                              default="school/images/default.png", null=True)
    
    def __str__(self):
        return self.ten_to
    
class City(models.Model):
    tinh_thanh = models.CharField(max_length=200)
    
    def __str__(self):
        return self.tinh_thanh
    
class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT)
    fullname = models.CharField(max_length=100, unique=False, default='')
    address = models.CharField(max_length=250, unique=False)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to = "school/images/", default = "school/images/ptnkavatar.png", null =True)
    
    def __str__(self):
        return self.user.username
    
    
class Contact(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True)
    subject = models.CharField(max_length=264)
    message = models.TextField()
    
    def __str__(self):
        return self.name + ", " + self.subject
    
    
class Admission(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, null=True)
    school = models.CharField(max_length=264)
    classroom = models.CharField(max_length=264, choices=[
    ('KC', 'Không Chuyên'),
    ('CT', 'Chuyên Toán'),
    ('CV', 'Chuyên Văn'),
    ('CL', 'Chuyên Lý'),
    ('CH', 'Chuyên Hóa'),
    ('CS', 'Chuyên Sinh'),
    ('CTin', 'Chuyên Tin'),
    ('CA', 'Chuyên Anh')
])   
    def __str__(self):
        return self.name + ", " + self.email
    
    
class Comment(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField(max_length=100, blank=True, default='')
    content = RichTextUploadingField(max_length=500)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE,null=True)
    created = models.DateTimeField(default=timezone.now)
    avatar = models.ImageField(upload_to = "school/images/", default = "school/images/ptnkavatar.png", null=True)
    isuser = models.BooleanField(default=False)
    total_likes = models.IntegerField(default=0)
    total_dislikes = models.IntegerField(default=0)
    
    class Meta:
        ordering = ('-created',)
      
    def __str__(self):
        return 'Bình luận của {} - {} - {}'.format(self.name, self.blog, self.isuser)
    
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    created = models.DateTimeField(default=timezone.now)
    islike = models.BooleanField(default=True)
    
    class Meta:
        ordering = ('-created',)
        
    def __str__(self):
        return self.islike
    

    

    
    
    
