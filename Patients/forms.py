from django import forms
from django.forms import formset_factory
# from bootstrap_datepicker_plus import DatePickerInput

class appointmentForm(forms.Form):
    first_name = forms.CharField(label='Firstname.**', required=False,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': False,
                                       'class': 'form-control',
                                       'placeholder': ('Firstname')
                                   }))
    last_name = forms.CharField(label='Lastname.**', required=False,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': False,
                                       'class': 'form-control',
                                       'placeholder': ('Lastname')
                                   }))                               
    requested_date = forms.DateField(label="Requested Date", required=False,
                                     widget=forms.widgets.DateInput(attrs={'type': 'date', 'class': 'form-control', }))

    #doctor_id = forms.IntegerField(label='Appointment With', required=True,
     #                                   widget=forms.NumberInput(attrs=
      #                                  {
       #                                     'required': False,
        #                                    'class': 'form-control',
         #                                   'placeholder': ('Appointment with')
          #                              }))
class insuranceClaimRequestForm(forms.Form):
    patient_firstname = forms.CharField(label='Firstname.**', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('patient_firstname')
                                   }))
                                   
    patient_lastname = forms.CharField(label='Lastname.**', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('patient_lastname')
                                   }))                               
    
    '''
    policy_name = forms.CharField(label='Insurance Policy Name', required=True,
                                   widget=forms.TextInput(attrs=
                                     {
                                         'required':True,

                                         'class': 'form-control',
                                         'placeholder': ('claim_amt')
                                     }))
    '''
    claim_amt = forms.IntegerField(label= 'Claim amount', required=True,
                                     widget=forms.NumberInput(attrs=
                                     {
                                         'required':True,
                                         'class': 'form-control',
                                         'placeholder': ('claim_amt')
                                     }))
class registerPolicyForm(forms.Form):
    
    patient_firstname = forms.CharField(label='Firstname', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('patient_firstname')
                                   }))
                                   
    patient_lastname = forms.CharField(label='Lastname', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('patient_lastname')
                                   }))         
   
    patient_age = forms.IntegerField(label='Age', required=True,
                                   widget=forms.NumberInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Age')
                                   }))                  

    patient_address = forms.CharField(label='Address', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Enter Address')
                                   }))
    patient_phone_no = forms.IntegerField(label='Phone', required=True,
                                   widget=forms.NumberInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Enter Phone Number')
                                   }))
    patient_email = forms.CharField(label='Email-id', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Enter Email')
                                   }))

class newInsurancePolicyForm(forms.Form):
    policy_name = forms.CharField(label='Policy Name', required=True,
                                   widget=forms.TextInput(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Policy Name')
                                   }))
    coverage_plans = forms.CharField(max_length = 200,label='Coverage Plans', required=True,
                                   widget = forms.Textarea(attrs=
                                   {
                                       'required': True,
                                       'class': 'form-control',
                                       'placeholder': ('Coverage Plans')
                                   }))                               
    insurance_amt = forms.IntegerField(label='Max Claim amount', required=True,
                                        widget=forms.NumberInput(attrs=
                                        {
                                            'required': True,
                                            'class': 'form-control',
                                            'placeholder': ('Max Claim amount')
                                        }))
    
class editForm(forms.Form):
    
    patient_name = forms.CharField(label='patient_name', required=True,
                                widget=forms.TextInput(attrs=
                                {
                                    'required': True,
                                    'class': 'form-control',
                                    'placeholder': ('Patient Name')
                                }))
    patient_age = forms.IntegerField(label='patient_age', required=True,
                                widget=forms.NumberInput(attrs=
                                {
                                    'required': True,
                                    'class': 'form-control',
                                    'placeholder': ('Patient Age')
                                }))
    patient_weight = forms.IntegerField(label='patient_weight', required=True,
                                widget=forms.NumberInput(attrs=
                                {
                                    'required': True,
                                    'class': 'form-control',
                                    'placeholder': ('Patient Weight')
                                }))
    patient_height = forms.IntegerField(label='patient_height', required=True,
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
    patient_phone_no = forms.IntegerField(label='patient_phone_no', required=True,
                                widget=forms.NumberInput(attrs=
                                {
                                    'required': True,
                                    'class': 'form-control',
                                    'placeholder': ('Patient Phone Number')
                                }))
    patient_email=forms.EmailField(max_length=50,required=False,label="Patient_Email",
                                    widget=forms.EmailInput(attrs=
                                    {
                                    'required': False,
                                    'class': 'form-control',
                                    'placeholder': ('Patient Email')
                                } ))

    