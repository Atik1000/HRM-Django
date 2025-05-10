from django import forms
from django.contrib.auth.models import User
from .models import Employee, Department

class EmployeeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    
    class Meta:
        model = Employee
        fields = ['employee_id', 'department', 'position', 'role', 'phone', 'address']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user_id:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

    def save(self, commit=True):
        employee = super().save(commit=False)
        if not employee.user_id:
            user = User.objects.create_user(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name']
            )
            employee.user = user
        else:
            employee.user.first_name = self.cleaned_data['first_name']
            employee.user.last_name = self.cleaned_data['last_name']
            employee.user.email = self.cleaned_data['email']
            employee.user.save()
            
        if commit:
            employee.save()
        return employee