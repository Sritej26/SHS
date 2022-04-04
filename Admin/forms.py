from django import forms

employee_depts= [
    ('Doctor', 'Doctor Staff'),
    ('Labstaff', 'Lab Staff'),
    ('Hospitalstaff', 'Hospital Staff'),
    ('Insurancestaff', 'Insurance Staff'),
    ]

class createEmployeeForm(forms.Form):
    employee_first_name = forms.CharField(label='First name', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('First name')
                                   }))
    employee_last_name = forms.CharField(label='Last name', required=True,
                                widget=forms.TextInput(attrs=
                                {
                                    'required': True,
                                    'class': 'form-control',
                                    'placeholder': ('Last name')
                                }))
    employee_email = forms.EmailField(label="Email", required=True,
                                widget=forms.TextInput(attrs=
                                {
                                    'required': True,
                                    'class': 'form-control',
                                    'placeholder': ('Email')
                                }))
    employee_dept = forms.ChoiceField(choices = employee_depts)

    
