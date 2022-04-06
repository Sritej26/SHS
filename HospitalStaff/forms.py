from django import forms
from django.forms import formset_factory

class patientDetailsForm(forms.Form):
    
    patient_name = forms.CharField(label='patient_name.**', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Patient Name')
                                   }))
    patient_age = forms.IntegerField(label='patient_age.**', required=True,
                                   widget=forms.NumberInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Patient Age')
                                   }))
    patient_weight = forms.IntegerField(label='patient_weight.**', required=True,
                                   widget=forms.NumberInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Patient Weight')
                                   }))
    patient_height = forms.IntegerField(label='patient_height.**', required=True,
                                   widget=forms.NumberInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Patient Height')
                                   }))
    patient_address = forms.CharField(label='patient_address.**', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Address')
                                   }))
    patient_phone_no = forms.IntegerField(label='patient_phone_no.**', required=True,
                                   widget=forms.NumberInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Patient Phone Number')
                                   }))
    patient_email = forms.CharField(label='patient_email.**', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Patient Email')
                                   }))
                                   
    # patient_disease = forms.CharField(label='patient_disease.**', required=True,
    #                                widget=forms.TextInput(attrs=
    #                                {
    #                                    'required': True,
    #                                    'class': 'form-control',
    #                                    'placeholder': ('Patient Disease')
    #                                }))
    # insurance_id = forms.IntegerField(label='insurance_id.**', required=True,
    #                                widget=forms.NumberInput(attrs=
    #                                {
    #                                    'required': True,
    #                                    'class': 'form-control',
    #                                    'placeholder': ('Insurance Id')
    #                                }))
    # patient_diagnosis = forms.CharField(label='patient_diagnosis.**', required=False,
    #                                widget=forms.TextInput(attrs=
    #                                {
    #                                    'required': False,
    #                                    'class': 'form-control',
    #                                    'placeholder': ('Patient Diagnosis')
    #                                }))
    # patient_reports = forms.CharField(label='patient_reports.**', required=False,
    #                                widget=forms.TextInput(attrs=
    #                                {
    #                                    'required': False,
    #                                    'class': 'form-control',
    #                                    'placeholder': ('Patent Reports')
    #                                }))
    # patient_prescription = forms.CharField(label='patient_prescription.**', required=False,
    #                                widget=forms.TextInput(attrs=
    #                                {
    #                                    'required': False,
    #                                    'class': 'form-control',
    #                                    'placeholder': ('Patient Prescription')
    #                                }))