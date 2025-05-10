from django.contrib import admin
from .models import Salary, Payroll

@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('employee', 'basic_salary', 'effective_date')
    search_fields = ('employee__user__username',)

@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('employee', 'month', 'gross_salary', 'net_salary', 'status')
    list_filter = ('status', 'month')
    search_fields = ('employee__user__username',)