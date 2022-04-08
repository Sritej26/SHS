from django import forms
from django.forms import formset_factory
 # from bootstrap_datepicker_plus import DatePickerInput
 
class Loginform(forms.Form):
     username = forms.CharField(label='username.**', required=True,
                                    widget=forms.TextInput(attrs=
                                    {
                                        'required': True,
                                        'class': 'form-control',
                                        'placeholder': ('username')
                                    }))
     password = forms.CharField(label='password.**', required=True,
                                    widget=forms.TextInput(attrs=
                                    {
                                        'required': True,
                                        'class': 'form-control',
                                        'placeholder': ('password')
                                    }))                               
     
class Registerform(forms.Form):
    patient_name = forms.CharField(label='Username.**', required=False,
                                    widget=forms.TextInput(attrs=
                                    {
                                        'required': False,
                                        'class': 'form-control',
                                        'placeholder': ('Enter Username')
                                    }))
    patient_age = forms.IntegerField(label='Age.**', required=False,
                                    widget=forms.NumberInput(attrs=
                                    {
                                        'required': False,
                                        'class': 'form-control',
                                        'placeholder': ('Age')
                                    }))                               
    patient_weight = forms.IntegerField(label='patient_weight.**', required=False,
                                    widget=forms.TextInput(attrs=
                                    {
                                        'required': False,
                                        'class': 'form-control',
                                        'placeholder': ('Enter Weight')
                                    }))
    patient_height = forms.IntegerField(label='patient_height.**', required=False,
                                    widget=forms.TextInput(attrs=
                                    {
                                        'required': False,
                                        'class': 'form-control',
                                        'placeholder': ('Enter height')
                                    }))
    patient_address = forms.CharField(label='patient_address.**', required=False,
                                    widget=forms.TextInput(attrs=
                                    {
                                        'required': False,
                                        'class': 'form-control',
                                        'placeholder': ('Enter Address')
                                    }))
    patient_phone_no = forms.IntegerField(label='patient_phone_no.**', required=False,
                                    widget=forms.NumberInput(attrs=
                                    {
                                        'required': False,
                                        'class': 'form-control',
                                        'placeholder': ('Enter Phone Number')
                                    }))
    patient_email = forms.CharField(label='patient_email.**', required=False,
                                    widget=forms.TextInput(attrs=
                                    {
                                        'required': False,
                                        'class': 'form-control',
                                        'placeholder': ('Enter Email')
                                    }))
    patient_card_details = forms.IntegerField(label='patient_card_details.**', required=False,
                                    widget=forms.NumberInput(attrs=
                                    {
                                        'required': False,
                                        'class': 'form-control',
                                        'placeholder': ('Enter Credit/Debit Card Details')
                                    }))
    User_password = forms.CharField(label='password.**', required=False,
                                    widget=forms.TextInput(attrs=
                                    {
                                        'required': False,
                                        'class': 'form-control',
                                        'placeholder': ('password')
                                    })) 
    passwordcheck = forms.CharField(label='password.**', required=False,
                                    widget=forms.TextInput(attrs=
                                    {
                                        'required': False,
                                        'class': 'form-control',
                                        'placeholder': ('Re-enter Password')
                                    })) 
     
     
