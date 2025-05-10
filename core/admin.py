from django.contrib import admin
from .models import PerformanceReview, Goal

@admin.register(PerformanceReview)
class PerformanceReviewAdmin(admin.ModelAdmin):
    list_display = ('employee', 'reviewer', 'review_period', 'performance_score', 'status')
    list_filter = ('status', 'review_period')
    search_fields = ('employee__user__username', 'reviewer__user__username')

@admin.register(Goal)
class GoalAdmin(admin.ModelAdmin):
    list_display = ('employee', 'title', 'due_date', 'status')
    list_filter = ('status',)
    search_fields = ('employee__user__username', 'title')
