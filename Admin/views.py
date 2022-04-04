from asyncio.log import logger
from django import conf
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from sklearn.datasets import load_files
from Admin.forms import createEmployeeForm
from Admin.models import EmployeeDetails
import logging
import os
from django.views.static import serve
from HospitalStaff.models import AppointmentDetails
from Hospitalportal.models import HospitalPortal
from django.core.mail import send_mail
from Doctors.models import DoctorDetails, prescriptions
from InsuranceStaff.models import InsuranceClaimDetails, InsurancePolicies
from LabStaff.models import LabReports

from Patients.models import PatientDetails

logger = logging.getLogger('django')

# Create your views here.
class adminHome(View):
    def get(self, request):
        return render(request, 'adminHome.html', {
            'user': 'Admin'
        })

class showLogFiles(View):
    def get(self, request):
        log_files = []
        for filename in os.listdir('/Users/harshilgandhi/Documents/CSE545/SHS_Grp14/logs'):
            with open(os.path.join('/Users/harshilgandhi/Documents/CSE545/SHS_Grp14/logs', filename), 'r') as file:
                log_files.append(filename)
        return render(request, 'showLogFiles.html', {
            'user': 'Admin',
            'log_files': log_files
        })
    def post(self, request):
        try:
            filename = request.POST.get('filename')
            response = HttpResponse()  
            response['X-File'] = '/Users/harshilgandhi/Documents/CSE545/SHS_Grp14/logs/' + filename 
            #https://stackoverflow.com/questions/1156246/having-django-serve-downloadable-files
            return response
        except:
            print('Cannot open file. Try again!')

class viewEmployeeRecords(View):
    def get(self, request):
        employeeDetails = EmployeeDetails.objects.all()
        return render(request, 'viewEmployeeRecords.html', {
            'user': 'Admin',
            'createEmployeeForm': createEmployeeForm,
            'employeeDetails': employeeDetails
        })

class createEmployeeRecords(View):
    def get(self, request):
        employeeDetails = EmployeeDetails.objects.all()
        return render(request, 'createEmployeeRecords.html', {
            'user': 'Admin',
            'createEmployeeForm': createEmployeeForm,
            'employeeDetails': employeeDetails
        })
    def post(self, request):
        msgS = ''
        try:
            form = createEmployeeForm(request.POST)
            if form.is_valid():
                employee_first_name = form.cleaned_data.get('employee_first_name')
                employee_last_name = form.cleaned_data.get('employee_last_name')
                employee_dept = form.cleaned_data.get('employee_dept')
                employee_email = form.cleaned_data.get('employee_email')
                send_mail(subject = 'Login credentials', message = 'Username: ' +  employee_first_name + ' Password: 12345678', from_email='admin@gmail.com', recipient_list=[employee_email])  
                print("going to save")
                EmployeeObj = EmployeeDetails(employee_first_name = employee_first_name, employee_last_name = employee_last_name, employee_email = employee_email, employee_dept = employee_dept)
                HospitalPortalObj = HospitalPortal(Role = employee_dept, username = employee_first_name, session = 'N')
                EmployeeObj.save()
                HospitalPortalObj.save()
                if employee_dept == 'Doctor':
                    DoctorObj = DoctorDetails(doctor_name = employee_first_name + ' ' + employee_last_name, doctor_spec = 'Physician', slot = 15)
                    DoctorObj.save()
                msgS = "Added Successfully"
            else:
                msgE = "Mention Name of the Application Type"
        except:
            msgE = "Something went Wrong"
        finally:
            messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR,
                                    (msgS if not msgS == '' else msgE),
                                    extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
            return redirect('/admin/createEmployeeRecords.html')

class editEmployeeRecords(View):
    def get(self, request):
        employeeDetails = EmployeeDetails.objects.all()
        return render(request, 'editEmployeeRecords.html', {
            'user': 'Admin',
            'createEmployeeForm': createEmployeeForm,
            'employeeDetails': employeeDetails
        })
    def post(self, request):
        msgS = ''
        try:
            form = createEmployeeForm(request.POST)
            if form.is_valid():
                employee_first_name = form.cleaned_data.get('employee_first_name')
                employee_last_name = form.cleaned_data.get('employee_last_name')
                employee_dept = form.cleaned_data.get('employee_dept')
                employee_email = form.cleaned_data.get('employee_email')
                print("going to save")
                EmployeeObj = EmployeeDetails(employee_first_name = employee_first_name, employee_last_name = employee_last_name, employee_email = employee_email, employee_dept = employee_dept)
                EmployeeObj.save()
                print("Saved")
                msgS = "Added Successfully"
            else:
                msgE = "Mention Name of the Application Type"
        except:
            print("in except block")
            msgE = "Something went Wrong"
        finally:
            print("in finally block")
            messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR,
                                    (msgS if not msgS == '' else msgE),
                                    extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
            return redirect('/admin/editEmployeeRecords.html')

class updateEmployeeDetails(View):
    def get(self, request, id):
        flag = 'false'
        print('hello')
        try:
            print("Entered try")
            details = EmployeeDetails.objects.get(employee_id=id)
            print(details)
            details = {'employee_id': details.employee_id,'employee_first_name': details.employee_first_name,'employee_last_name': details.employee_last_name, 'employee_email': details.employee_email, 'employee_dept': details.employee_dept}
            print(details)
        except:
            print('Error')
        finally:
            return render(request, 'updateEmployeeRecords.html', {'details': details, 'employeeDetailsForm': createEmployeeForm(details), "flag": flag})

    def post(self, request, id):
        msgS=''
        try:
            detail1 = EmployeeDetails.objects.get(employee_id = id)
            detailForm = createEmployeeForm(request.POST)
            print(detailForm.is_valid())
            if detailForm.is_valid():
                print("entered if")
                detail1.employee_first_name = request.POST.get('employee_first_name')
                detail1.employee_last_name = request.POST.get('employee_last_name')
                detail1.employee_dept = request.POST.get('employee_dept')
                detail1.employee_email = request.cleaned_data.get('employee_email')
                detail1.save()
                messages.success(request, 'Employee Details Updated Successfully!')
        except:
            messages.error(request, 'Something Went Wrong!')
        finally:
            flag = 'true'
            print(detail1.employee_id)
            employeeDetails = EmployeeDetails.objects.all()
            print(employeeDetails)
            return redirect('/admin/editEmployeeRecords.html')

class deleteEmployeeRecord(View):
    def get(self, request, id):
        try:
            details = EmployeeDetails.objects.get(employee_id=id)
            details.delete()
            logger.info('Record deleted')
        except:
            print('Error')
        finally:
            return redirect('/admin/editEmployeeRecords.html')
    
    def post(self, request):
        pass

class appointmentTransactionRequests(View):
    def get(self, request):
        try:
            appointmentDetails = AppointmentDetails.objects.all()
        except:
            print('Error loading data')
        finally:
            return render(request, 'appointmentTransactionRequests.html', {
                'appointmentTransactions': appointmentDetails
            })
    
    def post(seld, request):
        try:
            appointment_id = int(request.POST.get('approve'))
            AppointmentObj = AppointmentDetails.objects.get(appointment_id=appointment_id)
            AppointmentObj.transaction_status = "Done"
            AppointmentObj.save()
        except:
            print('Error')
        finally:
            return redirect('/admin/appointmentTransactionRequests.html')
    
class insuranceTransactionRequests(View):
    def get(self, request):
        try:
            insuranceDetails = InsuranceClaimDetails.objects.all()
        except:
            print('Error loading data')
        finally:
            return render(request, 'insuranceTransactionRequests.html', {
                'insuranceTransactions': insuranceDetails
            })

    def post(self, request):
        try:
            claim_id = int(request.POST.get('approve'))
            InsuranceObj = InsuranceClaimDetails.objects.get(claim_id=claim_id)
            patient_id = InsuranceObj.patient_id
            PatientObj = PatientDetails.objects.get(patient_id=patient_id)
            send_mail(subject = 'Bill', message = 'Hello, ' + InsuranceObj.patient_firstname + ' Claimed amount: ' +  str(InsuranceObj.claim_amt), from_email='admin@gmail.com', recipient_list=[PatientObj.patient_email])  
            print('sent mail')
            InsuranceObj.claim_transaction_status = "Done"
            InsuranceObj.save()
        except:
            print('Error')
        finally:
            return redirect('/admin/insuranceTransactionRequests.html') 

class showInternalFiles(View):
    def get(self, request):
        try:
            patient_details = PatientDetails.objects.all()
        except:
            print('Error loading data')
        finally:
            return render(request, 'showInternalFiles.html', {
                'patient_details': patient_details
            })

class showHospitalFiles(View):
    def get(self, request):
        try:
            appointment_details = AppointmentDetails.objects.all()
        except:
            print('Error loading data')
        finally:
            return render(request, 'showHospitalFiles.html', {
                'appointment_details': appointment_details
            })

class showInsuranceFiles(View):
     def get(self, request):
        try:
            policy_details = InsurancePolicies.objects.all()
            claim_details = InsuranceClaimDetails.objects.all()
        except:
            print('Error loading data')
        finally:
            return render(request, 'showInsuranceFiles.html', {
                'policy_details': policy_details,
                'claim_details': claim_details
            })

class showLabFiles(View):
    def get(self, request):
        try:
            lab_details = LabReports.objects.all()
        except:
            print('Error loading data')
        finally:
            return render(request, 'showLabFiles.html', {
                'lab_details': lab_details
            })

class showDoctorFiles(View):
    def get(self, request):
        try:
            prescription_details = prescriptions.objects.all()
        except:
            print('Error loading data')
        finally:
            return render(request, 'showDoctorFiles.html', {
                'prescription_details': prescription_details
            })