from django.urls import path
from . import views

app_name = 'report'
urlpatterns = [
    path('', views.dashboard_with_pivot, name='dashboard_with_pivot'),
    path('result/', views.pivot_data, name='pivot_data'),
    path('student/', views.pivot_data2, name='pivot_data2'),
    path('summary/', views.summary, name='summary.html'),
    path('statistic/', views.stats, name='statistic.html'),
]
