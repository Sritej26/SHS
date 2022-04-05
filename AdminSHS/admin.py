from django.contrib import admin
from .models import AdminDetails, EmployeeDetails, TransactionDetails

# Register your models here.
admin.site.register(AdminDetails)
admin.site.register(EmployeeDetails)
admin.site.register(TransactionDetails)
