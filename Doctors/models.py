from django.db import models

# Create your models here.
class DoctorDetails(models.Model):
    doctor_id = models.AutoField(primary_key=True)
    doctor_name = models.CharField(max_length=1000, null=False)
    doctor_spec = models.CharField(max_length=1000, null=False)
    slot = models.IntegerField(default=10, null=False)

class prescriptions(models.Model):
    patient_id = models.IntegerField(default=0, null=False)
    appointment_id = models.IntegerField(null=False)
    first_name = models.CharField(max_length=1000, null=False)
    last_name = models.CharField(max_length=1000, null=False)
    requested_date = models.DateField(blank=True, null=True)
    doctor_id = models.IntegerField(default=0, null=False)
    patient_diagnosis = models.CharField(max_length=255, default="")
    drug = models.CharField(max_length=255, default="")
    unit = models.CharField(max_length=255, default="")
    dosage = models.IntegerField(max_length=255, default="")
    prescription_text = models.CharField(max_length=255, default="")

class labTests(models.Model):
    patient_id = models.IntegerField(default=0, null=False)
    appointment_id = models.IntegerField(null=False)
    first_name = models.CharField(max_length=1000, null=False)
    last_name = models.CharField(max_length=1000, null=False)
    requested_date = models.DateField(blank=True, null=True)
    doctor_id = models.IntegerField(default=0, null=False)
    patient_diagnosis = models.CharField(max_length=255, default="")
    lab_test = models.CharField(max_length=255, default="")
    lab_report = models.CharField(max_length=255, default="")
    lab_test_status = models.CharField(max_length=255, default="")
    lab_report_status = models.CharField(max_length=255, default="")

