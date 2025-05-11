from django import forms
from .models import Salary, Payroll

class SalaryForm(forms.ModelForm):
    class Meta:
        model = Salary
        fields = ['employee', 'basic_salary', 'allowances', 'deductions', 'effective_date']
        widgets = {
            'effective_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = ['employee', 'month', 'year', 'basic_salary', 'allowances', 
                 'deductions', 'overtime_hours', 'overtime_rate']
        widgets = {
            'month': forms.Select(choices=[(i, i) for i in range(1, 13)]),
            'year': forms.Select(choices=[(i, i) for i in range(2020, 2031)]),
        }

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data.get('overtime_hours') and not cleaned_data.get('overtime_rate'):
            raise forms.ValidationError("Overtime rate is required when overtime hours are specified.")
        return cleaned_data