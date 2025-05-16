from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import JobPosting, JobApplication, Interview
from .forms import JobPostingForm, JobApplicationForm, InterviewForm

@login_required
def job_list(request):
    jobs = JobPosting.objects.all().order_by('-created_at')
    return render(request, 'recruitment/job_list.html', {'jobs': jobs})

@login_required
def job_detail(request, pk):
    job = get_object_or_404(JobPosting, pk=pk)
    applications = job.jobapplication_set.all()
    return render(request, 'recruitment/job_detail.html', {
        'job': job,
        'applications': applications
    })

@login_required
def job_create(request):
    if request.method == 'POST':
        form = JobPostingForm(request.POST)
        if form.is_valid():
            job = form.save()
            messages.success(request, 'Job posting created successfully.')
            return redirect('recruitment:job_detail', pk=job.pk)
    else:
        form = JobPostingForm()
    return render(request, 'recruitment/job_form.html', {'form': form})

@login_required
def application_list(request):
    applications = JobApplication.objects.all().order_by('-applied_at')
    return render(request, 'recruitment/application_list.html', {'applications': applications})

@login_required
def application_detail(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    interviews = application.interview_set.all()
    return render(request, 'recruitment/application_detail.html', {
        'application': application,
        'interviews': interviews
    })

@login_required
def schedule_interview(request, application_pk):
    application = get_object_or_404(JobApplication, pk=application_pk)
    if request.method == 'POST':
        form = InterviewForm(request.POST)
        if form.is_valid():
            interview = form.save(commit=False)
            interview.application = application
            interview.save()
            messages.success(request, 'Interview scheduled successfully.')
            return redirect('recruitment:application_detail', pk=application_pk)
    else:
        form = InterviewForm()
    return render(request, 'recruitment/interview_form.html', {
        'form': form,
        'application': application
    })

@login_required
def dashboard(request):
    context = {
        'open_positions': JobPosting.objects.filter(status='published').count(),
        'total_applications': JobApplication.objects.count(),
        'scheduled_interviews': Interview.objects.filter(status='scheduled').count(),
        'selected_candidates': JobApplication.objects.filter(status='selected').count(),
        'recent_applications': JobApplication.objects.order_by('-applied_at')[:10]
    }
    return render(request, 'recruitment/dashboard.html', context)

@login_required
def update_application_status(request, pk):
    application = get_object_or_404(JobApplication, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(JobApplication.STATUS_CHOICES):
            application.status = new_status
            application.save()
            messages.success(request, 'Application status updated successfully.')
    return redirect('recruitment:application_detail', pk=pk)