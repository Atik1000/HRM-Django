from django.db import models
from django.db.models import Sum
from employees.models import Employee

class Salary(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    effective_date = models.DateField()

    @property
    def net_salary(self):
        return self.basic_salary + self.allowances - self.deductions

    def calculate_overtime_pay(self, hours, rate):
        return hours * rate

    class Meta:
        ordering = ['-effective_date']

class Payroll(models.Model):
    PENDING = 'pending'
    PROCESSED = 'processed'
    PAID = 'paid'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (PROCESSED, 'Processed'),
        (PAID, 'Paid'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.IntegerField()
    year = models.IntegerField()
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overtime_hours = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    overtime_rate = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def overtime_pay(self):
        return self.overtime_hours * self.overtime_rate

    @property
    def total_deductions(self):
        return self.deductions

    @property
    def net_salary(self):
        return (self.basic_salary + self.allowances + self.overtime_pay) - self.total_deductions

    def generate_payslip(self):
        return {
            'employee': self.employee,
            'month': self.month,
            'year': self.year,
            'basic_salary': self.basic_salary,
            'allowances': self.allowances,
            'deductions': self.deductions,
            'overtime_pay': self.overtime_pay,
            'net_salary': self.net_salary,
        }

    class Meta:
        ordering = ['-year', '-month']
        unique_together = ['employee', 'month', 'year']