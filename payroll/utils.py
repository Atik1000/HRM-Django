from decimal import Decimal
from datetime import datetime
from .models import Salary, Payroll

def calculate_monthly_payroll(employee, month, year, overtime_hours=0, overtime_rate=0):
    try:
        salary = Salary.objects.get(employee=employee)
        payroll = Payroll(
            employee=employee,
            month=month,
            year=year,
            basic_salary=salary.basic_salary,
            allowances=salary.allowances,
            deductions=salary.deductions,
            overtime_hours=overtime_hours,
            overtime_rate=overtime_rate
        )
        return payroll
    except Salary.DoesNotExist:
        return None

def generate_payroll_report(month, year):
    payrolls = Payroll.objects.filter(month=month, year=year)
    total_basic = sum(p.basic_salary for p in payrolls)
    total_allowances = sum(p.allowances for p in payrolls)
    total_deductions = sum(p.total_deductions for p in payrolls)
    total_overtime = sum(p.overtime_pay for p in payrolls)
    total_net = sum(p.net_salary for p in payrolls)

    return {
        'month': month,
        'year': year,
        'total_employees': payrolls.count(),
        'total_basic': total_basic,
        'total_allowances': total_allowances,
        'total_deductions': total_deductions,
        'total_overtime': total_overtime,
        'total_net': total_net,
        'payrolls': payrolls
    }