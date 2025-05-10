from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.attendance_list, name='list'),
    path('mark/', views.mark_attendance, name='mark'),
    path('leave/', views.leave_list, name='leave_list'),
    path('leave/request/', views.leave_request, name='leave_request'),
]