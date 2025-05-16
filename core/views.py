from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from employees.models import Employee
from attendance.models import Attendance
from recruitment.models import JobPosting

@login_required
def dashboard(request):
    context = {
        'total_employees': request.user.employee_set.count() if request.user.role in ['admin', 'hr'] else 0,
        'pending_leaves': Leave.objects.filter(status='pending').count() if request.user.role in ['admin', 'hr', 'manager'] else 0,
        'active_jobs': JobPosting.objects.filter(status='published').count(),
    }
    return render(request, 'core/dashboard.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('core:dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'authentication/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('core:login')
