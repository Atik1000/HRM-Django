from django.contrib import admin
from .models import JobPosting, Candidate

@admin.register(JobPosting)
class JobPostingAdmin(admin.ModelAdmin):
    list_display = ('title', 'department', 'status', 'closing_date')
    list_filter = ('status', 'department')
    search_fields = ('title',)

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'job', 'status', 'applied_date')
    list_filter = ('status', 'job')
    search_fields = ('first_name', 'last_name', 'email')