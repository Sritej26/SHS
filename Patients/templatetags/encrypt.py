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
        #id = signing.loads(id)
        return signing.dumps(username.employee_id)
    except:
        return ''
@register.filter
def name_from_id(k,a):
    try:
        patient_name= PatientDetails.objects.get(patient_id=a).patient_name
        return patient_name
    except:
        return ''

@register.filter
def getDocname(k,a):
    try:
        docDetails = DoctorDetails.objects.all()
        doc_id_list = []
        for i in docDetails :
                doc_id_list.append(i.doctor_id)
        if a in doc_id_list:
            doc = DoctorDetails.objects.get(doctor_id=a)
            #id = signing.loads(id)
            return doc.doctor_name
        else:
            return 'Unavailable - left organization'

    except:
        return ''
