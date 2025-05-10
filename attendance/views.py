from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Attendance, Leave
from .forms import AttendanceForm, LeaveForm
from employees.models import Employee

@login_required
def attendance_list(request):
    today = timezone.now().date()
    attendances = Attendance.objects.filter(date=today).select_related('employee__user')
    return render(request, 'attendance/attendance_list.html', {'attendances': attendances})

@login_required
def mark_attendance(request):
    if request.method == 'POST':
        form = AttendanceForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Attendance marked successfully.')
            return redirect('attendance:list')
    else:
        form = AttendanceForm()
    return render(request, 'attendance/attendance_form.html', {'form': form})

@login_required
def leave_request(request):
    if request.method == 'POST':
        form = LeaveForm(request.POST)
        if form.is_valid():
            leave = form.save(commit=False)
            leave.employee = request.user.employee
            leave.save()
            messages.success(request, 'Leave request submitted successfully.')
            return redirect('attendance:leave_list')
    else:
        form = LeaveForm()
    return render(request, 'attendance/leave_form.html', {'form': form})

@login_required
def leave_list(request):
    if request.user.employee.role in ['hr', 'manager']:
        leaves = Leave.objects.all().select_related('employee__user')
    else:
        leaves = Leave.objects.filter(employee=request.user.employee)
    return render(request, 'attendance/leave_list.html', {'leaves': leaves})