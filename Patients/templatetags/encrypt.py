from django import template
from django.core import signing
from Patients.models import *
from AdminSHS.models import EmployeeDetails

register=template.Library()

@register.filter
def patient_id_encrypt_tag(k,a):
    try:
        return signing.dumps(a)
    except:
        return ''

@register.filter
def getHospitalStaffId(k,a):
    try:
        username = EmployeeDetails.objects.get(employee_username=a)
        return username.employee_id
    except:
        return ''

@register.filter
def name_from_id(k,a):
    try:
        patient_name= PatientDetails.objects.get(patient_id=a).patient_name
        return patient_name
    except:
        return ''