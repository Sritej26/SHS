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
from django.contrib.auth import logout
import datetime
from Patients.models import PatientDetails
import requests
import json
import re

regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

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

def logout_user(request,id):
    logout(request)
    return redirect(reverse('Login'))
    #logger.info("USERNAME:  " username.patient_name "   LOGOUTIME:   "+dt_string)
    
def selectDepartment(id):
    if signing.loads(id) == 1:
        department = 'Doctor'
    elif signing.loads(id) == 2:
        department = 'Labstaff'
    elif signing.loads(id) == 3:
        department = 'Hospitalstaff'
    elif signing.loads(id) == 4:
        department = 'Insurancestaff'
    
    return department

# Create your views here.
class adminHome(View):
    def get(self, request, id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        id = signing.loads(id)
        adminName = User.objects.get(id=id)
        return render(request, 'adminHome.html', {
            'user': adminName.username,
            'id': id
        })

class showLogFiles(View):
    def get(self, request, id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        id = signing.loads(id)
        adminName = User.objects.get(id=id)
        log_files = []
        for filename in os.listdir('/Users/harshilgandhi/Documents/CSE545/SHS_Grp14/logs'):
            with open(os.path.join('/Users/harshilgandhi/Documents/CSE545/SHS_Grp14/logs', filename), 'r') as file:
                log_files.append(filename)
        return render(request, 'showLogFiles.html', {
            'user': adminName.username,
            'log_files': log_files,
            'id': id
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
    def get(self, request, id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        employeeDetails = EmployeeDetails.objects.all()
        emails = []
        for employee in employeeDetails:
            employee.employee_email = unmask(employee.employee_email)
        id = signing.loads(id)
        adminName = User.objects.get(id=id)
        return render(request, 'viewEmployeeRecords.html', {
            'user': adminName.username,
            'createEmployeeForm': createEmployeeForm,
            'employeeDetails': employeeDetails,
            'id': id
        })

class createEmployeeRecords(View):
    def get(self, request, id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        id = signing.loads(id)
        adminName = User.objects.get(id=id)
        return render(request, 'createEmployeeRecords.html', {
            'user': adminName.username,
            'createEmployeeForm': createEmployeeForm,
            'id': id
        })
    def post(self, request, id):
        msgS = ''
        msgE = []
        error = 0
        try:
            form = createEmployeeForm(request.POST)
            if form.is_valid():
                employee_first_name = form.cleaned_data.get('employee_first_name')
                employee_last_name = form.cleaned_data.get('employee_last_name')
                employee_username = form.cleaned_data.get('employee_username')
                employee_dept = form.cleaned_data.get('employee_dept')
                employee_email = mask(form.cleaned_data.get('employee_email'))
                if not request.POST.get('employee_first_name'):
                     msgE.append( "First Name is Mandatory")
                     error=error+1
                if not request.POST.get('employee_last_name'):
                     msgE.append( "Last Name is Mandatory")
                     error=error+1
                if not request.POST.get('employee_username'):
                    msgE.append( "Username is Mandatory")
                    error=error+1
                if not request.POST.get('employee_email'):
                    msgE.append( "Email is Mandatory")
                    error=error+1
                if request.POST.get('employee_email'):
                    if re.fullmatch(regex, employee_email):
                        print('valid email')
                    else:
                        msgE.append("Please enter a valid email")
                        error+=1
                if signing.loads(employee_dept) == 0:
                    print('came here')
                    msgE.append('Departnemt is required')
                    error += 1
                if User.objects.filter(email = unmask(employee_email)).exists() or EmployeeDetails.objects.filter(employee_email = employee_email).exists():
                    msgE.append('Email already exists. Try another email')
                    error+=1
                if EmployeeDetails.objects.filter(employee_username = employee_username).exists() or User.objects.filter(username = employee_username).exists():
                    msgE.append('Username already exists. Try another username')
                    error+=1
                if error >= 1:
                    exit()
                else:
                    password = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 10))
                    Userobj = User.objects.create_user(username=employee_username, password = password, email = unmask(employee_email), first_name = employee_first_name, last_name = employee_last_name)
                    Userobj.save()
                    to_send_email = unmask(employee_email)
                    send_mail(subject = 'Login credentials', message = 'Username: ' +  employee_username + ' Password: ' + password, from_email='admin@gmail.com', recipient_list=[to_send_email])
                    send_action_email(Userobj,request)
                    messages.info(request,'Please check your email to verify the account')
                    EmployeeObj = EmployeeDetails(employee_first_name = employee_first_name, employee_last_name = employee_last_name, employee_username = employee_username, employee_email = employee_email, employee_dept = selectDepartment(employee_dept))
                    EmployeeObj.save()
                    msgS = "Added Successfully"
            else:
                msgE.append("Something went wrong")
        except:
            msgE = msgE
        finally:
            messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR,
                                    (msgS if not msgS == '' else msgE),
                                    extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
            return HttpResponseRedirect(reverse('AdminSHS:createEmployeeRecords', args=[id]))
            
class editEmployeeRecords(View):
    def get(self, request, id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        employeeDetails = EmployeeDetails.objects.all()
        id = signing.loads(id)
        adminName = User.objects.get(id=id)
        for employee in employeeDetails:
            employee.employee_email = unmask(employee.employee_email)
        return render(request, 'editEmployeeRecords.html', {
            'user': adminName.username,
            'createEmployeeForm': createEmployeeForm,
            'employeeDetails': employeeDetails,
            'id': id
        })

    def post(self, request):
       pass

class updateEmployeeDetails(View):
    def get(self, request, id, a_id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
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
                'user': adminName.username
            })

    def post(self, request, id, a_id):
        msgS=''
        msgE = []
        error = 0
        try:
            id = signing.loads(id)
            a_id = signing.loads(a_id)
            detail1 = EmployeeDetails.objects.get(employee_id = a_id)
            detailForm = editEmployeeForm(request.POST)
            if detailForm.is_valid():
                detail1.employee_first_name = request.POST.get('employee_first_name')
                detail1.employee_last_name = request.POST.get('employee_last_name')
                detail1.employee_dept = request.POST.get('employee_dept')
                if not request.POST.get('employee_first_name'):
                     msgE.append( "First Name is Mandatory")
                     error+=1
                if not request.POST.get('employee_last_name'):
                     msgE.append( "Last Name is Mandatory")
                     error+=1
                if signing.loads(detail1.employee_dept) == 0:
                    msgE.append('Departnemt is required')
                    error += 1
                if error >= 1:
                    exit()
                else:
                    userObj = User.objects.get(username=detail1.employee_username)
                    userObj.first_name = detail1.employee_first_name
                    userObj.last_name = detail1.employee_last_name
                    userObj.save()
                    if HospitalPortal.objects.filter(username=detail1.employee_username).exists():
                        hospitalObj = HospitalPortal.objects.get(username=detail1.employee_username)
                        hospitalObj.Role = selectDepartment(detail1.employee_dept) 
                        hospitalObj.save()
                    if selectDepartment(detail1.employee_dept) == 'Doctor':
                        if DoctorDetails.objects.filter(doctor_username = detail1.employee_username).exists():
                            DoctorObj = DoctorDetails.objects.get(doctor_username = detail1.employee_username)
                            DoctorObj.doctor_name = detail1.employee_first_name
                            DoctorObj.doctor_spec = 'Physician'
                            DoctorObj.slot = 15
                            DoctorObj.save()
                        elif DoctorDetails.objects.filter(doctor_username = detail1.employee_username).exists() and HospitalPortal.objects.filter(username=detail1.employee_username).exists():
                            DoctorObj = DoctorDetails(doctor_name = detail1.employee_first_name, doctor_spec = 'Physician', slot = 15, doctor_username = detail1.employee_username)
                            DoctorObj.save()
                    if selectDepartment(detail1.employee_dept) != 'Doctor':
                        if DoctorDetails.objects.filter(doctor_username = detail1.employee_username).exists():
                            DoctorObj = DoctorDetails.objects.get(doctor_username = detail1.employee_username)
                            DoctorObj.delete()
                    detail1.save()
                    messages.success(request, 'Employee Details Updated Successfully!')
            else:
                msgE.append("Something went wrong")
        except:
            msgE = msgE
            messages.error(request, 'Something Went Wrong!')
        finally:
            flag = 'true'
            id = signing.dumps(id)
            employeeDetails = EmployeeDetails.objects.all()
            # return redirect('/adminSHS/editEmployeeRecords.html')
            return HttpResponseRedirect(reverse('adminSHS:editEmployeeRecords', args=[id]))

class deleteEmployeeRecord(View):
    def get(self, request, id, a_id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        try:
            id = signing.loads(id)
            a_id = signing.loads(a_id)
            employee = EmployeeDetails.objects.get(employee_id=a_id)
            userObj = User.objects.get(username = employee.employee_username)
            userObj.delete()
            if HospitalPortal.objects.filter(username = employee.employee_username).exists():
                hospitalObj = HospitalPortal.objects.get(username = employee.employee_username)
                hospitalObj.delete()
            if employee.employee_dept == 'Doctor':
                if DoctorDetails.objects.filter(doctor_username = employee.employee_username).exists():
                    doctor = DoctorDetails.objects.get(doctor_username = employee.employee_username)
                    doctor.delete()
            employee.delete()
            logger.info('Record deleted')
        except:
            print('Error')
        finally:
            id = signing.dumps(id)
            return HttpResponseRedirect(reverse('adminSHS:editEmployeeRecords', args=[id]))
    
    def post(self, request):
        pass

class appointmentTransactionRequests(View):
    def get(self, request, id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
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
                'user': adminName.username
            })
    
    def post(self, request, id):
        try:
            msgS=""
            id = signing.loads(id)
            approve_id = request.POST.get("approve")
            deny_id = request.POST.get("deny")
            if approve_id != None:
                AppointmentObj = AppointmentDetails.objects.get(appointment_id=approve_id)
                PatientObj = PatientDetails.objects.get(patient_id=AppointmentObj.patient_id)
                send_mail(subject = 'Bill', message = 'Hello, ' + AppointmentObj.first_name + ' $300 has been deducted from your account with card details: ' +  str(PatientObj.card_details), from_email='admin@gmail.com', recipient_list=[PatientObj.patient_email])  
                AppointmentObj.transaction_status = "Done"
                AppointmentObj.save()
                ledgerobj = {"amount": 300, "patientId":AppointmentObj.patient_id, "purpose": "appointment","transactionId": AppointmentObj.transactionId,"from":fromid,"__transaction":AppointmentObj.transactionId}
                headers={'APIKEY':API_KEY,"Accept":"application/json",'Content-Type':'application/json'}
                r=requests.post(url=API_BLOCK_CHAIN, data=json.dumps(ledgerobj), headers=headers)
                msgS="Transaction Added to the HyperLedger"
            if deny_id != None:
                AppointmentObj = AppointmentDetails.objects.get(appointment_id=deny_id)
                PatientObj = PatientDetails.objects.get(patient_id=AppointmentObj.patient_id)
                send_mail(subject = 'Bill', message = 'Hello, ' + AppointmentObj.first_name + ' your transaction is declined.', from_email='admin@gmail.com', recipient_list=[PatientObj.patient_email])  
                AppointmentObj.transaction_status = "Declined"
                AppointmentObj.save()
        except:
            print('Error')
        finally:
            messages.success(request, 'Transaction Added to the HyperLedger!')
            id = signing.dumps(id)
            return HttpResponseRedirect(reverse('adminSHS:appointmentTransactionRequests', args=[id]))
    
class insuranceTransactionRequests(View):
    def get(self, request, id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
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
                'user': adminName.username
            })

    def post(self, request, id):
        try:
            id = signing.loads(id)
            approve_id = request.POST.get("approve")
            deny_id = request.POST.get("deny")
            print('362')
            if approve_id != None:
                InsuranceObj = InsuranceClaimDetails.objects.get(claim_id=approve_id)
                patient_id = InsuranceObj.patient_id
                PatientObj = PatientDetails.objects.get(patient_id=patient_id)
                send_mail(subject = 'Insurance claimed', message = 'Hello, ' + InsuranceObj.patient_firstname + ' Claim amount of ' +  str(InsuranceObj.claim_amt) + ' has been applied to your account.', from_email='admin@gmail.com', recipient_list=[PatientObj.patient_email])  
                print('sent mail')
                ledgerobj = {"amount": InsuranceObj.claim_amt, "patientId":InsuranceObj.patient_id, "purpose": "Claim","transactionId": InsuranceObj.claim_transaction_id,"from":fromid,"__transaction":InsuranceObj.claim_transaction_id}
                headers={'APIKEY':API_KEY,"Accept":"application/json",'Content-Type':'application/json'}
                r=requests.post(url=API_BLOCK_CHAIN, data=json.dumps(ledgerobj), headers=headers)
                InsuranceObj.claim_transaction_status = "Done"
                InsuranceObj.save()
            if deny_id != None:
                InsuranceObj = InsuranceClaimDetails.objects.get(claim_id=deny_id)
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
            id = signing.dumps(id)
            return HttpResponseRedirect(reverse('adminSHS:insuranceTransactionRequests', args=[id]))

class showInternalFiles(View):
    def get(self, request, id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
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
                'user': adminName.username
            })

class showHospitalFiles(View):
    def get(self, request, id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
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
                'user': adminName.username
            })

class showInsuranceFiles(View):
     def get(self, request, id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
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
                'user': adminName.username
            })

class showLabFiles(View):
    def get(self, request, id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
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
                'user': adminName.username
            })

class showDoctorFiles(View):
    def get(self, request, id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
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
                'user': adminName.username
            })