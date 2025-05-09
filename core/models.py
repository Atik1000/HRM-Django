from django.db import models
from employees.models import Employee

class PerformanceReview(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reviews_given')
    review_period = models.CharField(max_length=50)  # e.g., "Q1 2023"
    review_date = models.DateField()
    performance_score = models.DecimalField(max_digits=3, decimal_places=2)
    strengths = models.TextField()
    areas_for_improvement = models.TextField()
    goals = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('acknowledged', 'Acknowledged')
    ])

class Goal(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('overdue', 'Overdue')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
