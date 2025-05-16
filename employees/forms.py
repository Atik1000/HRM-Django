from django import forms
from django.contrib.auth import get_user_model
from .models import Employee, Department

User = get_user_model()

class EmployeeForm(forms.ModelForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    phone = forms.CharField(max_length=20)
    department = forms.ModelChoiceField(queryset=Department.objects.all())
    position = forms.CharField(max_length=100)
    hire_date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    salary = forms.DecimalField(max_digits=10, decimal_places=2)
    address = forms.CharField(widget=forms.Textarea)
    emergency_contact = forms.CharField(max_length=100)
    emergency_phone = forms.CharField(max_length=20)

    class Meta:
        model = Employee
        fields = ['position', 'hire_date', 'salary', 'address', 
                 'emergency_contact', 'emergency_phone']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user_id:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['phone'].initial = self.instance.user.phone
            self.fields['department'].initial = self.instance.user.department

    def save(self, commit=True):
        employee = super().save(commit=False)
        if not employee.user_id:
            user = User.objects.create_user(
                username=self.cleaned_data['email'],
                email=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                phone=self.cleaned_data['phone']
            )
            user.department = self.cleaned_data['department']
            user.save()
            employee.user = user
        else:
            user = employee.user
            user.first_name = self.cleaned_data['first_name']
            user.last_name = self.cleaned_data['last_name']
            user.email = self.cleaned_data['email']
            user.phone = self.cleaned_data['phone']
            user.department = self.cleaned_data['department']
            user.save()
        
        if commit:
            employee.save()
        return employee