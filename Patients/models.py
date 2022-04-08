import imp
from django.db import models
from Doctors.models import DoctorDetails

# Create your models here.
class PatientDetails(models.Model):
    patient_id = models.AutoField(primary_key=True)
    patient_name = models.CharField(max_length=100, null=False)
    patient_age = models.IntegerField(null=False)
    patient_weight = models.IntegerField(max_length=100, null=False)
    patient_height = models.IntegerField(max_length=100, null=False)
    patient_address = models.CharField(max_length=1000, null=False)
    patient_phone_no = models.IntegerField(null=False)
    patient_email = models.CharField(max_length=100,null=True)
    change_request_status = models.IntegerField(default=0)
    request_info = models.CharField(max_length=1000, default="")
    card_details = models.IntegerField(null=False)
  
    
    