from django.contrib import admin
from .models import Department, Employee

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'get_department', 'position', 'hire_date', 'get_phone')
    list_filter = ('user__department', 'hire_date')
    search_fields = ('user__first_name', 'user__last_name', 'position')
    raw_id_fields = ('user',)

    def get_department(self, obj):
        return obj.user.department
    get_department.short_description = 'Department'
    
    def get_phone(self, obj):
        return obj.user.phone
    get_phone.short_description = 'Phone'

    def full_name(self, obj):
        return obj.user.get_full_name()
    full_name.short_description = 'Employee Name'