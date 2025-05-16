from django.contrib import admin
from .models import JobPosting, JobApplication, Interview

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'status', 'created_at')
    list_filter = ('status', 'department')
    search_fields = ('title', 'description')

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('applicant_name', 'job', 'status', 'applied_at')
    list_filter = ('status', 'job')
    search_fields = ('applicant_name', 'email')

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('application', 'interviewer', 'scheduled_at', 'status')
    list_filter = ('status', 'interviewer')
    search_fields = ('application__applicant_name',)