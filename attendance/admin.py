from django.contrib import admin
from .models import Attendance, Leave

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee', 'date', 'check_in', 'check_out', 'status')
    list_filter = ('status', 'date')
    search_fields = ('employee__user__username',)

@admin.register(Leave)
class LeaveAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date', 'leave_type', 'status')
    list_filter = ('status', 'leave_type')
    search_fields = ('employee__user__username',)