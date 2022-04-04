from statistics import mode
from django.db import models

# Create your models here.
class LabReports(models.Model):
    report_id = models.AutoField(primary_key=True)
    report_info = models.CharField(max_length=5000, null=True)
    doctor_id = models.IntegerField(null=False)
    patient_id = models.IntegerField(null=False)
    patient_diagnosis = models.CharField(max_length=1000, default="")
    lab_staff_id = models.IntegerField(null=False)
    report_status = models.CharField(max_length=100, null=False)
    test_name = models.CharField(max_length=255, null=True)