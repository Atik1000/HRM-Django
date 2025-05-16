from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('hr', 'HR Manager'),
        ('manager', 'Department Manager'),
        ('employee', 'Employee'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    department = models.ForeignKey('employees.Department', on_delete=models.SET_NULL, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    phone = models.CharField(max_length=20, blank=True)

    class Meta:
        permissions = [
            ("can_view_dashboard", "Can view dashboard"),
            ("can_manage_employees", "Can manage employees"),
            ("can_manage_recruitment", "Can manage recruitment"),
            ("can_manage_payroll", "Can manage payroll"),
            ("can_manage_attendance", "Can manage attendance"),
            ("can_manage_performance", "Can manage performance"),
        ]

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    link = models.CharField(max_length=200, blank=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class PerformanceReview(models.Model):
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey('employees.Employee', on_delete=models.CASCADE, related_name='reviews_given')
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
    employee = models.ForeignKey('employees.Employee', on_delete=models.CASCADE)
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
