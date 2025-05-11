from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Salary, Payroll
from .forms import SalaryForm, PayrollForm
from employees.models import Employee

@login_required
def salary_list(request):
    salaries = Salary.objects.select_related('employee__user').all()
    return render(request, 'payroll/salary_list.html', {'salaries': salaries})

@login_required
def salary_create(request):
    if request.method == 'POST':
        form = SalaryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Salary details added successfully.')
            return redirect('payroll:salary_list')
    else:
        form = SalaryForm()
    return render(request, 'payroll/salary_form.html', {'form': form})

@login_required
def payroll_list(request):
    payrolls = Payroll.objects.select_related('employee__user').all()
    return render(request, 'payroll/payroll_list.html', {'payrolls': payrolls})

@login_required
def process_payroll(request):
    if request.method == 'POST':
        form = PayrollForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Payroll processed successfully.')
            return redirect('payroll:payroll_list')
    else:
        form = PayrollForm()
    return render(request, 'payroll/payroll_form.html', {'form': form})