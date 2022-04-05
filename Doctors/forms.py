from django import forms
from django.forms import formset_factory

class patientDetailsForm(forms.Form):
    patient_id = forms.IntegerField(label='patient_id.**', required=True,
                                   widget=forms.NumberInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('PatientId'),
                                       'readonly': 'readonly'
                                   }))
    patient_name = forms.CharField(label='patient_name.**', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Patient Name'),
                                       'readonly': 'readonly'
                                   }))
    patient_age = forms.IntegerField(label='patient_age.**', required=True,
                                   widget=forms.NumberInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Patient Age'),
                                       'readonly': 'readonly'
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
    
    
    
class diagnosisForm(forms.Form):
    patient_diagnosis = forms.CharField(label='patient_diagnosis.**', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Patient Diagnosis')
                                   }))

Lab_Tests= [
    ('Complete Blood Count', 'Complete Blood Count'),
    ('Prothrombin Time', 'Prothrombin Time'),
    ('Basic Metabolic Panel', 'Basic Metabolic Panel'),
    ('Comprehensive Metabolic Panel', 'Comprehensive Metabolic Panel'),
    ('Lipid Panel','Lipid Panel'),
    ('Liver Panel','Liver Panel'),
    ('Thyroid Stimulating Hormone','Thyroid Stimulating Hormone'),
    ('Hemoglobin A1C','Hemoglobin A1C'),
    ('Urinalysis','Urinalysis')
    ]

class labTestsForm(forms.Form):
    lab_tests = forms.ChoiceField(choices = Lab_Tests)
            
class datePicker(forms.Form):
    date_picker = forms.DateField(label="Date Picker", required=False,
                                     widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control', }))

class patientDiagnosisForm(forms.Form):
    patient_id = forms.IntegerField(label='patient_id.**', required=True,
                                   widget=forms.NumberInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('PatientId'),
                                       'readonly': 'readonly'
                                   }))
    appointment_id = forms.IntegerField(label='appointment_id.**', required=True,
                                   widget=forms.NumberInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Appointment Id'),
                                       'readonly': 'readonly'
                                   }))
    first_name = forms.CharField(label='first_name.**', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('First Name'),
                                       'readonly': 'readonly'
                                   }))
    last_name = forms.CharField(label='last_name.**', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Last Name'),
                                       'readonly': 'readonly'
                                   }))
    doctor_id = forms.IntegerField(label='doctor_id.**', required=True,
                                   widget=forms.NumberInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Doctor Id'),
                                       'readonly': 'readonly'
                                   }))
    requested_date = forms.DateField(label="Requested Date", required=False,
                                     widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control','readonly': 'readonly' }))
    status = forms.CharField(label='status.**', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Status'),
                                       'readonly': 'readonly'
                                   }))
    patient_diagnosis = forms.CharField(label='patient_diagnosis.**', required=False,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': False,
                                       'class': 'form-control',
                                       'placeholder': ('Patient Diagnosis')
                                   }))
    
class patientPrescriptionForm(forms.Form):
    drug = forms.CharField(label='drug.**', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Drug')
                                   }))
    unit = forms.CharField(label='unit.**', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Tablet/Syrup')
                                   }))
    dosage = forms.IntegerField(label='dosage.**', required=True,
                                   widget=forms.NumberInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Dosage')
                                   }))
    prescription_text = forms.CharField(label='prescription_text.**', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('prescription_text')
                                   }))

class appointmentForm(forms.Form):
    first_name = forms.CharField(label='Firstname.**', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Firstname')
                                   }))
    last_name = forms.CharField(label='Lastname.**', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Lastname')
                                   }))                               
    requested_date = forms.DateField(label="Requested Date", required=False,
                                     widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control', }))

    doctor_id = forms.IntegerField(label='Appointment With', required=True,
                                        widget=forms.NumberInput(attrs=
                                        {
                                            'required': False,
                                            'class': 'form-control',
                                            'placeholder': ('Appointment with')
                                        }))