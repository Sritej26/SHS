from cmath import sin
from dis import dis
from django import forms
from django.core import signing
from numpy import sign
employee_depts= [
    (signing.dumps(0), '--Select--'),
    (signing.dumps(1), 'Doctor Staff'),
    (signing.dumps(2), 'Lab Staff'),
    (signing.dumps(3), 'Hospital Staff'),
    (signing.dumps(4), 'Insurance Staff'),
    ]

class createEmployeeForm(forms.Form):
    employee_first_name = forms.CharField(label='First name',
                                   widget=forms.TextInput(attrs=
                                   {
                                       'class': 'form-control',
                                       'placeholder': ('First name')
                                   }))
    employee_last_name = forms.CharField(label='Last name',
                                widget=forms.TextInput(attrs=
                                {
                                    'class': 'form-control',
                                    'placeholder': ('Last name'),
                                }))
    employee_username = forms.CharField(label='Username',
                                widget=forms.TextInput(attrs=
                                {
                                    'class': 'form-control',
                                    'placeholder': ('Username')
                                }))
    employee_email = forms.EmailField(label="Email",
                                widget=forms.TextInput(attrs=
                                {
                                    'class': 'form-control',
                                    'placeholder': ('Email')
                                }))
    employee_dept = forms.ChoiceField(choices = employee_depts, label="Department")

    
class editEmployeeForm(forms.Form):
    employee_first_name = forms.CharField(label='First name',
                                   widget=forms.TextInput(attrs=
                                   {
                                       'class': 'form-control',
                                       'placeholder': ('First name')
                                   }))
    employee_last_name = forms.CharField(label='Last name',
                                widget=forms.TextInput(attrs=
                                {
                                    'class': 'form-control',
                                    'placeholder': ('Last name'),
                                }))
    # employee_username = forms.CharField(label='Username', required=True, disabled=True,
    #                             widget=forms.TextInput(attrs=
    #                             {
    #                                 'required': True,
    #                                 'class': 'form-control',
    #                                 'placeholder': ('Username')
    #                             }))
    # employee_email = forms.EmailField(label="Email", required=True, disabled=True,
    #                             widget=forms.TextInput(attrs=
    #                             {
    #                                 'required': True,
    #                                 'class': 'form-control',
    #                                 'placeholder': ('Email')
    #                             }))
    employee_dept = forms.ChoiceField(choices = employee_depts, label="Department")