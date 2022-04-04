from django.db import models
from django.core.validators import validate_email

# Create your models here.
class InsuranceClaimDetails(models.Model):
    claim_id = models.AutoField(primary_key=True)
    patient_id = models.IntegerField(null=False)
    patient_firstname = models.CharField(max_length=100, null=False, default="fn")
    patient_lastname = models.CharField(max_length=100, null=False, default="ln")
    policy_name =  models.CharField(max_length=1000, null=False)
    claim_status = models.CharField(max_length=100, null=False, default="Pending")
    claim_amt = models.IntegerField(null=False)
    claim_transaction_status = models.CharField(max_length=100, null=False, default="null")
    claim_transaction_id = models.CharField(max_length=100, null=False, default="#C")

class InsurancePolicies(models.Model):
    policy_id = models.AutoField(primary_key=True)
    policy_name = models.CharField(max_length=1000, null=False)
    coverage_plans = models.CharField(max_length=1000, null=False)
    insurance_amt = models.IntegerField(default=0, null=False)

class InsuranceClaimRegister(models.Model):
    patient_id = models.IntegerField(null=False)
    patient_firstname = models.CharField(max_length=100, null=False, default="fn")
    patient_lastname = models.CharField(max_length=100, null=False, default="ln")
    # policy_id = models.ForeignKey(InsurancePolicies,on_delete=models.CASCADE)
    policy_id = models.IntegerField(null=False)
    patient_age = models.IntegerField(null=False, max_length=3)
    patient_address = models.CharField(max_length=1000, null=False)
    patient_phone_no = models.IntegerField(null=False, max_length=10)
    patient_email = models.EmailField(null=True, validators=[validate_email])

