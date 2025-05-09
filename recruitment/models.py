from django.db import models
from employees.models import Department

class JobPosting(models.Model):
    title = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField()
    requirements = models.TextField()
    salary_range = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('closed', 'Closed')
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    closing_date = models.DateField()

class Candidate(models.Model):
    job = models.ForeignKey(JobPosting, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    resume = models.FileField(upload_to='resumes/')
    status = models.CharField(max_length=20, choices=[
        ('applied', 'Applied'),
        ('screening', 'Screening'),
        ('interview', 'Interview'),
        ('offered', 'Offered'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired')
    ])
    applied_date = models.DateTimeField(auto_now_add=True)