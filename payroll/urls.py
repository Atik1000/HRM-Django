from django.urls import path
from . import views

app_name = 'payroll'

urlpatterns = [
    path('salary/', views.salary_list, name='salary_list'),
    path('salary/create/', views.salary_create, name='salary_create'),
    path('payroll/', views.payroll_list, name='payroll_list'),
    path('payroll/process/', views.process_payroll, name='process_payroll'),
]