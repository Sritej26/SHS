from asyncio.log import logger
from django.urls import reverse
from django import conf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
from matplotlib import use
from numpy import sign
from sklearn.datasets import load_files
from AdminSHS.forms import createEmployeeForm, editEmployeeForm
from AdminSHS.models import EmployeeDetails
import logging
import os
from django.views.static import serve
from HospitalStaff.models import AppointmentDetails
from Hospitalportal.models import HospitalPortal
from django.core.mail import send_mail
from Doctors.models import DoctorDetails, prescriptions
from Hospitalportal.views import User
from InsuranceStaff.models import InsuranceClaimDetails, InsurancePolicies
from LabStaff.models import LabReports
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from .utils import generate_token
from django.utils.encoding import force_bytes,force_str,force_str,DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.conf import settings
import threading
import string
import random
from HospitalStaff.helper import mask,unmask
from django.core import signing

from Patients.models import PatientDetails
import requests
logger = logging.getLogger('django')
#DJango authentication
API_BLOCK_CHAIN = "https://api.simbachain.com/v1/HospitalTxn/payed/"
API_KEY = "006d9b97dd5817c45d47bd308b7fe19417cb613c9d1b98c8088dd237247b28d7"
fromid="3D3F18C2DBD834039C0C4D6251AECCD7D30B7B1B"
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

def send_action_email(user, request):
    current_site=get_current_site(request)
    email_subject = 'Activate your account'
    email_body=render_to_string('activate.html',{
        'user':user,
        'domain':current_site,
        'uid':urlsafe_base64_encode(force_bytes(user.pk)),
        'token':generate_token.make_token(user)

    })

    email = EmailMessage(subject=email_subject, body=email_body,from_email=settings.EMAIL_FROM_USER,to=[user.email])

    if getattr(settings, 'TESTING', True):
        EmailThread(email).start()

# Create your views here.
class adminHome(View):
    def get(self, request, id):
        id = signing.loads(id)
        adminName = User.objects.get(id=id)
        print(adminName.first_name)
        return render(request, 'adminHome.html', {
            'user': adminName.first_name,
            'id': id
        })

class showLogFiles(View):
    def get(self, request, id):
        id = signing.loads(id)
        adminName = User.objects.get(id=id)
        log_files = []
        for filename in os.listdir('/Users/harshilgandhi/Documents/CSE545/SHS_Grp14/logs'):
            with open(os.path.join('/Users/harshilgandhi/Documents/CSE545/SHS_Grp14/logs', filename), 'r') as file:
                log_files.append(filename)
        return render(request, 'showLogFiles.html', {
            'user': adminName.first_name,
            'log_files': log_files,
            'id': id
        })
    def post(self, request, id):
        try:
            id = signing.loads(id)
            print(id)
            filename = request.POST.get('filename')
            response = HttpResponse()  
            response['X-File'] = '/Users/harshilgandhi/Documents/CSE545/SHS_Grp14/logs/' + filename 
            #https://stackoverflow.com/questions/1156246/having-django-serve-downloadable-files
            return response
        except:
            print('Cannot open file. Try again!')

class viewEmployeeRecords(View):
    def get(self, request, id):
        employeeDetails = EmployeeDetails.objects.all()
        id = signing.loads(id)
        adminName = User.objects.get(id=id)
        return render(request, 'viewEmployeeRecords.html', {
            'user': adminName.first_name,
            'createEmployeeForm': createEmployeeForm,
            'employeeDetails': employeeDetails,
            'id': id
        })

class createEmployeeRecords(View):
    def get(self, request, id):
        id = signing.loads(id)
        adminName = User.objects.get(id=id)
        return render(request, 'createEmployeeRecords.html', {
            'user': adminName.first_name,
            'createEmployeeForm': createEmployeeForm,
            'id': id
        })
    def post(self, request, id):
        msgS = ''
        try:
            form = createEmployeeForm(request.POST)
            if form.is_valid():
                employee_first_name = form.cleaned_data.get('employee_first_name')
                employee_last_name = form.cleaned_data.get('employee_last_name')
                employee_username = form.cleaned_data.get('employee_username')
                employee_dept = form.cleaned_data.get('employee_dept')
                employee_email = mask(form.cleaned_data.get('employee_email'))
                if User.objects.filter(email = unmask(employee_email)).exists():
                    msgE = 'Email already exists. Try another email'
                elif EmployeeDetails.objects.filter(employee_email = employee_email).exists():
                    msgE = 'Email already exists. Try another email'
                elif EmployeeDetails.objects.filter(employee_username = employee_username).exists():
                    msgE = 'Username already exists. Try another username'
                else:
                    password = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
                    Userobj = User.objects.create_user(username=employee_username, password = password, email = unmask(employee_email))
                    Userobj.save()
                    to_send_email = unmask(employee_email)
                    send_mail(subject = 'Login credentials', message = 'Username: ' +  employee_username + ' Password: ' + password, from_email='admin@gmail.com', recipient_list=[to_send_email])
                    send_action_email(Userobj,request)
                    messages.info(request,'Please check your email to verify the account')
                    EmployeeObj = EmployeeDetails(employee_first_name = employee_first_name, employee_last_name = employee_last_name, employee_username = employee_username, employee_email = employee_email, employee_dept = employee_dept)
                    EmployeeObj.save()
                    msgS = "Added Successfully"
            else:
                msgE = "Mention Name of the Application Type"
        except:
            msgE = "Something went Wrong"
        finally:
            # id = signing.dumps(id)
            messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR,
                                    (msgS if not msgS == '' else msgE),
                                    extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
            # return redirect('/adminSHS/createEmployeeRecords.html')
            return HttpResponseRedirect(reverse('AdminSHS:createEmployeeRecords', args=[id]))
            
class editEmployeeRecords(View):
    def get(self, request, id):
        employeeDetails = EmployeeDetails.objects.all()
        id = signing.loads(id)
        adminName = User.objects.get(id=id)
        return render(request, 'editEmployeeRecords.html', {
            'user': adminName.first_name,
            'createEmployeeForm': createEmployeeForm,
            'employeeDetails': employeeDetails,
            'id': id
        })

    def post(self, request):
       pass

class updateEmployeeDetails(View):
    def get(self, request, id, a_id):
        flag = 'false'
        try:
            id = signing.loads(id)
            a_id = signing.loads(a_id)
            adminName = User.objects.get(id=id)
            EmployeeObj = EmployeeDetails.objects.get(employee_id=a_id)
            details = {'employee_id': EmployeeObj.employee_id,'employee_first_name': EmployeeObj.employee_first_name,'employee_last_name': EmployeeObj.employee_last_name, 'employee_username': EmployeeObj.employee_username, 'employee_email': unmask(EmployeeObj.employee_email), 'employee_dept': EmployeeObj.employee_dept}
        except:
            print('Error')
        finally:
            return render(request, 'updateEmployeeRecords.html', {
                'details': details, 
                'employeeDetailsForm': editEmployeeForm(details), 
                'flag': flag, 
                'id': id, 
                'user': adminName.first_name
            })

    def post(self, request, id, a_id):
        msgS=''
        try:
            id = signing.loads(id)
            a_id = signing.loads(a_id)
            detail1 = EmployeeDetails.objects.get(employee_id = a_id)
            detailForm = editEmployeeForm(request.POST)
            if detailForm.is_valid():
                detail1.employee_first_name = request.POST.get('employee_first_name')
                detail1.employee_last_name = request.POST.get('employee_last_name')
                detail1.employee_dept = request.POST.get('employee_dept')
                if detail1.employee_dept == 'Doctor':
                        DoctorObj = DoctorDetails.objects.get(doctor_username = detail1.employee_username)
                        DoctorObj.doctor_name = detail1.employee_first_name
                        DoctorObj.doctor_spec = 'Physician'
                        DoctorObj.slot = 15
                        DoctorObj.save()
                detail1.save()
                messages.success(request, 'Employee Details Updated Successfully!')
        except:
            messages.error(request, 'Something Went Wrong!')
        finally:
            flag = 'true'
            id = signing.dumps(id)
            employeeDetails = EmployeeDetails.objects.all()
            # return redirect('/adminSHS/editEmployeeRecords.html')
            return HttpResponseRedirect(reverse('adminSHS:editEmployeeRecords', args=[id]))

class deleteEmployeeRecord(View):
    def get(self, request, id, a_id):
        try:
            id = signing.loads(id)
            a_id = signing.loads(a_id)
            employee = EmployeeDetails.objects.get(employee_id=a_id)
            if employee.employee_dept == 'Doctor':
                doctor = DoctorDetails.objects.get(doctor_username = employee.employee_username)
                doctor.delete()
            user = User.objects.get(email=unmask(employee.employee_email))
            employee.delete()
            user.delete()
            logger.info('Record deleted')
        except:
            print('Error')
        finally:
            id = signing.dumps(id)
            return HttpResponseRedirect(reverse('adminSHS:editEmployeeRecords', args=[id]))
    
    def post(self, request):
        pass

class appointmentTransactionRequests(View):
    def get(self, request, id, a_id):
        try:
            appointmentDetails = AppointmentDetails.objects.all()
            id = signing.loads(id)
            adminName = User.objects.get(id=id)
        except:
            print('Error loading data')
        finally:
            return render(request, 'appointmentTransactionRequests.html', {
                'appointmentTransactions': appointmentDetails,
                'id': id,
                'user': adminName.first_name
            })
    
    def post(self, request, id, a_id):
        try:
            msgS=""
            id = signing.loads(id)
            a_id = signing.loads(a_id)
            approve = request.POST.get("approve")
            if approve != None:
                appointment_id = a_id
                AppointmentObj = AppointmentDetails.objects.get(appointment_id=appointment_id)
                PatientObj = PatientDetails.objects.get(patient_id=AppointmentObj.patient_id)
                send_mail(subject = 'Bill', message = 'Hello, ' + AppointmentObj.first_name + ' $300 has been deducted from your account with card details: ' +  str(PatientObj.card_details), from_email='admin@gmail.com', recipient_list=[PatientObj.patient_email])  
                ledgerobj = {"amount": 300, "patientId":AppointmentObj.patient_id, "purpose": "appointment","transactionId": AppointmentObj.transactionId,"from":fromid,"__transaction":AppointmentObj.transactionId}
                headers={'APIKEY':API_KEY,"Accept":"application/json",'Content-Type':'application/json'}
                r=requests.post(url=API_BLOCK_CHAIN, data=json.dumps(ledgerobj), headers=headers)
                msgS="Transaction Added to the HyperLedger"
                AppointmentObj.transaction_status = "Done"
                AppointmentObj.save()
            else:
                appointment_id = a_id
                AppointmentObj = AppointmentDetails.objects.get(appointment_id=appointment_id)
                PatientObj = PatientDetails.objects.get(patient_id=AppointmentObj.patient_id)
                send_mail(subject = 'Bill', message = 'Hello, ' + AppointmentObj.first_name + ' your transaction is declined.', from_email='admin@gmail.com', recipient_list=[PatientObj.patient_email])  
                AppointmentObj.transaction_status = "Declined"
                AppointmentObj.save()
        except:
            print('Error')
            msgE="Transaction Added to the HyperLedger"
        finally:
            messages.success(request, 'Transaction Added to the HyperLedger!')
            id = signing.dumps(id)
            return HttpResponseRedirect(reverse('adminSHS:appointmentTransactionRequests', args=[id]))
    
class insuranceTransactionRequests(View):
    def get(self, request, id, a_id):
        try:
            insuranceDetails = InsuranceClaimDetails.objects.all()
            id = signing.loads(id)
            adminName = User.objects.get(id=id)
        except:
            print('Error loading data')
        finally:
            return render(request, 'insuranceTransactionRequests.html', {
                'insuranceTransactions': insuranceDetails,
                'id': id,
                'user': adminName.first_name
            })

    def post(self, request, id, a_id):
        try:
            id = signing.loads(id)
            a_id = signing.loads(a_id)
            approve = request.POST.get("approve")
            if approve != None:
                claim_id = a_id
                InsuranceObj = InsuranceClaimDetails.objects.get(claim_id=claim_id)
                patient_id = InsuranceObj.patient_id
                PatientObj = PatientDetails.objects.get(patient_id=patient_id)
                send_mail(subject = 'Insurance claimed', message = 'Hello, ' + InsuranceObj.patient_firstname + ' Claim amount of ' +  str(InsuranceObj.claim_amt) + ' has been applied to your account.', from_email='admin@gmail.com', recipient_list=[PatientObj.patient_email])  
                print('sent mail')
                ledgerobj = {"amount": InsuranceObj.claim_amt, "patientId":InsuranceObj.patient_id, "purpose": "Claim","transactionId": InsuranceObj.claim_transaction_id,"from":fromid,"__transaction":InsuranceObj.claim_transaction_id}
                headers={'APIKEY':API_KEY,"Accept":"application/json",'Content-Type':'application/json'}
                r=requests.post(url=API_BLOCK_CHAIN, data=json.dumps(ledgerobj), headers=headers)
                InsuranceObj.claim_transaction_status = "Done"
                InsuranceObj.save()
            else:
                claim_id = a_id
                InsuranceObj = InsuranceClaimDetails.objects.get(claim_id=claim_id)
                patient_id = InsuranceObj.patient_id
                PatientObj = PatientDetails.objects.get(patient_id=patient_id)
                send_mail(subject = 'Insurance claimed', message = 'Hello, ' + InsuranceObj.patient_firstname + ' Your insurance claim is declined ', from_email='admin@gmail.com', recipient_list=[PatientObj.patient_email])  
                print('sent mail')
                InsuranceObj.claim_transaction_status = "Declined"
                InsuranceObj.save()
        except:
            print('Error')
            messages.success(request, 'Transaction Added to the HyperLedger!')
        finally:
            messages.success(request, 'Transaction Added to the HyperLedger!')
            return HttpResponseRedirect(reverse('adminSHS:insuranceTransactionRequests', args=[id]))

class showInternalFiles(View):
    def get(self, request, id):
        try:
            patient_details = PatientDetails.objects.all()
            id = signing.loads(id)
            adminName = User.objects.get(id=id)
        except:
            print('Error loading data')
        finally:
            return render(request, 'showInternalFiles.html', {
                'patient_details': patient_details,
                'id': id,
                'user': adminName.first_name
            })

class showHospitalFiles(View):
    def get(self, request, id):
        try:
            appointment_details = AppointmentDetails.objects.all()
            id = signing.loads(id)
            adminName = User.objects.get(id=id)
        except:
            print('Error loading data')
        finally:
            return render(request, 'showHospitalFiles.html', {
                'appointment_details': appointment_details,
                'id': id,
                'user': adminName.first_name
            })

class showInsuranceFiles(View):
     def get(self, request, id):
        try:
            policy_details = InsurancePolicies.objects.all()
            claim_details = InsuranceClaimDetails.objects.all()
            id = signing.loads(id)
            adminName = User.objects.get(id=id)
        except:
            print('Error loading data')
        finally:
            return render(request, 'showInsuranceFiles.html', {
                'policy_details': policy_details,
                'claim_details': claim_details,
                'id': id,
                'user': adminName.first_name
            })

class showLabFiles(View):
    def get(self, request, id):
        try:
            lab_details = LabReports.objects.all()
            id = signing.loads(id)
            adminName = User.objects.get(id=id)
        except:
            print('Error loading data')
        finally:
            return render(request, 'showLabFiles.html', {
                'lab_details': lab_details,
                'id': id,
                'user': adminName.first_name
            })

class showDoctorFiles(View):
    def get(self, request, id):
        try:
            prescription_details = prescriptions.objects.all()
            id = signing.loads(id)
            adminName = User.objects.get(id=id)
        except:
            print('Error loading data')
        finally:
            return render(request, 'showDoctorFiles.html', {
                'prescription_details': prescription_details,
                'id': id,
                'user': adminName.first_name
            })