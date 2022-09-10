from django.urls import path
from . import views

app_name = 'school'
urlpatterns = [
    path('', views.index, name='index.html'),
    path('contact/', views.contact, name='contact.html'),
    path('profile/', views.profile, name='profile.html'),
    path('doanthe/<int:pk>/', views.doanthe, name='doanthe.html'),
    path('doanthe-detail/<int:pk>/', views.doanthe_detail, name='doanthe-detail.html'),
    path('blog/<int:pk>/', views.blog, name='blog.html'),
    path('feeds/', views.feeds, name='feeds.html'),
    path('blog-detail/<int:pk>/', views.blog_detail, name='blog-detail.html'),
    path('info-detail/<int:pk>/', views.info_detail, name='info-detail.html'),
    path('result/', views.result, name='result.html'),
    path('entrance-score/', views.entrance_score, name='entrance-score.html'),
    path('search/', views.search, name='search.html'),
    path('library/', views.library, name='library.html'),
    path('register/', views.register, name='register.html'),
    path('login/', views.log_in, name='login.html'),
    path('log_out/', views.log_out, name='log_out'),
    path('document/<int:pk>/', views.document, name='document.html'),
    path('tobomon/<int:pk>/', views.tobomon, name='tobomon.html'),
    path('tobomon-detail/<int:pk>/', views.tobomon_detail, name='tobomon-detail.html'),
    path('banchuyentrach/<int:pk>/', views.bct, name='bct.html'),
    path('gioithieu/', views.intro, name='intro.html'),
    path('info/<int:pk>/', views.info, name='info.html'),
    path('entrance/', views.entrance, name='entrance.html'),
]
