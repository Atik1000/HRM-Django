from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Attendance
from employees.models import Employee

@login_required
def attendance_list(request):
    try:
        if request.user.role in ['admin', 'hr']:
            # Admin and HR can see all attendances
            attendances = Attendance.objects.select_related('employee__user').all()
        else:
            # Regular employees see their own attendance
            employee = Employee.objects.get(user=request.user)
            attendances = Attendance.objects.filter(employee=employee)
        
        context = {
            'attendances': attendances,
            'today': timezone.now().date()
        }
        return render(request, 'attendance/attendance_list.html', context)
    except Employee.DoesNotExist:
        messages.error(request, "Employee profile not found.")
        return redirect('core:dashboard')

@login_required
def check_in(request):
    try:
        employee = Employee.objects.get(user=request.user)
        today = timezone.now().date()
        
        attendance, created = Attendance.objects.get_or_create(
            employee=employee,
            date=today,
            defaults={
                'status': 'present',
                'check_in': timezone.now()
            }
        )
        
        if not created:
            if not attendance.check_out:
                attendance.check_out = timezone.now()
                attendance.save()
                messages.success(request, 'Check-out recorded successfully.')
            else:
                messages.warning(request, 'You have already checked out for today.')
        else:
            messages.success(request, 'Check-in recorded successfully.')
            
        return redirect('attendance:list')
    except Employee.DoesNotExist:
        messages.error(request, "Employee profile not found.")
        return redirect('core:dashboard')