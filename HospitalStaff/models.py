from django.db import models

# Create your models here.
class AppointmentDetails(models.Model):
    appointment_id = models.AutoField(primary_key=True)
    patient_id = models.IntegerField(null=False)
    first_name = models.CharField(max_length=255,default="fn")
    last_name = models.CharField(max_length=255,default="ln")
    doctor_id = models.IntegerField(null=False, default=0)
    requested_date = models.DateField(blank=True, null=True)
    prescribed_report_status = models.BooleanField(default=False)                       # patient comes -> takes appointment -> this field will be by default "False" -> when doctor prescribes test changed to "True". Those changed to "True" will be shown under lab requests
    report_status = models.CharField(null=False, max_length=255, default="Pending")                                 # whether the lab report request is "approved" by the patient or not
    status =models.CharField(max_length=255,default="Pending")
    patient_diagnosis = models.CharField(max_length=255, default="")
    transaction_status =models.CharField(max_length=255,default="null")
    transaction_id = models.CharField(max_length=100, null=False, default="#C")