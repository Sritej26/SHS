from operator import mod
from statistics import mode
#from tkinter import N
#from tkinter import N
from django.db import models

# Create your models here.
class AdminDetails(models.Model):
    admin_id = models.IntegerField(null=False)
    admin_name = models.CharField(max_length=100, null=False)

class EmployeeDetails(models.Model):
    employee_id = models.AutoField(primary_key=True)
    employee_first_name = models.CharField(max_length=255, null=False)
    employee_last_name = models.CharField(max_length=255, null=False)
    employee_email = models.EmailField(null=False)
    employee_dept = models.CharField(max_length=255, null=False)

class TransactionDetails(models.Model):
    transaction_id = models.IntegerField(null=False)
    amount = models.IntegerField(null=False)
    patient_id = models.IntegerField(null=False)
    transaction_info = models.CharField(max_length=100, null=False)
    transaction_status = models.CharField(max_length=100, null=False)
    receipt_info = models.CharField(max_length=100)