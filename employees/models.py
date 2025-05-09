from django.db import models
from django.contrib.auth.models import User

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Employee(models.Model):
    ROLE_CHOICES = [
        ('staff', 'Staff'),
        ('manager', 'Manager'),
        ('hr', 'HR'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    employee_id = models.CharField(max_length=10, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')
    position = models.CharField(max_length=100)
    date_joined = models.DateField()
    phone = models.CharField(max_length=15)
    address = models.TextField()
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.employee_id}"