from asyncio.log import logger
from audioop import reverse
from django import conf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views import View
from django.contrib import messages
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

logger = logging.getLogger('django')

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
    def get(self, request):
        return render(request, 'adminHome.html', {
            'user': 'AdminSHS'
        })

class showLogFiles(View):
    def get(self, request):
        log_files = []
        for filename in os.listdir('/Users/harshilgandhi/Documents/CSE545/SHS_Grp14/logs'):
            with open(os.path.join('/Users/harshilgandhi/Documents/CSE545/SHS_Grp14/logs', filename), 'r') as file:
                log_files.append(filename)
        return render(request, 'showLogFiles.html', {
            'user': 'AdminSHS',
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
            'user': 'AdminSHS',
            'createEmployeeForm': createEmployeeForm,
            'employeeDetails': employeeDetails
        })

class createEmployeeRecords(View):
    def get(self, request):
        return render(request, 'createEmployeeRecords.html', {
            'user': 'AdminSHS',
            'createEmployeeForm': createEmployeeForm
        })
    def post(self, request):
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
                    Userobj = User.objects.create_user(username=employee_first_name, password = password, email = unmask(employee_email))
                    Userobj.save()
                    to_send_email = unmask(employee_email)
                    send_mail(subject = 'Login credentials', message = 'Username: ' +  employee_username + ' Password: ' + password, from_email='admin@gmail.com', recipient_list=[to_send_email])
                    send_action_email(Userobj,request)
                    messages.info(request,'Please check your email to verify the account')
                    EmployeeObj = EmployeeDetails(employee_first_name = employee_first_name, employee_last_name = employee_last_name, employee_username = employee_username, employee_email = employee_email, employee_dept = employee_dept)
                    EmployeeObj.save()
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
            return redirect('/adminSHS/createEmployeeRecords.html')

class editEmployeeRecords(View):
    def get(self, request):
        employeeDetails = EmployeeDetails.objects.all()
        return render(request, 'editEmployeeRecords.html', {
            'user': 'AdminSHS',
            'createEmployeeForm': createEmployeeForm,
            'employeeDetails': employeeDetails
        })
    def post(self, request):
       pass

class updateEmployeeDetails(View):
    def get(self, request, id):
        flag = 'false'
        print('hello')
        try:
            id = signing.loads(id)
            print("Entered try")
            EmployeeObj = EmployeeDetails.objects.get(employee_id=id)
            details = {'employee_id': EmployeeObj.employee_id,'employee_first_name': EmployeeObj.employee_first_name,'employee_last_name': EmployeeObj.employee_last_name, 'employee_username': EmployeeObj.employee_username, 'employee_email': unmask(EmployeeObj.employee_email), 'employee_dept': EmployeeObj.employee_dept}
        except:
            print('Error')
        finally:
            return render(request, 'updateEmployeeRecords.html', {'details': details, 'employeeDetailsForm': editEmployeeForm(details), "flag": flag})

    def post(self, request, id):
        msgS=''
        try:
            id = signing.loads(id)
            detail1 = EmployeeDetails.objects.get(employee_id = id)
            detailForm = editEmployeeForm(request.POST)
            print(detailForm.is_valid())
            if detailForm.is_valid():
                detail1.employee_first_name = request.POST.get('employee_first_name')
                detail1.employee_last_name = request.POST.get('employee_last_name')
                detail1.employee_dept = request.POST.get('employee_dept')
                detail1.save()
                messages.success(request, 'Employee Details Updated Successfully!')
        except:
            messages.error(request, 'Something Went Wrong!')
        finally:
            flag = 'true'
            id = signing.dumps(id)
            employeeDetails = EmployeeDetails.objects.all()
            return redirect('/adminSHS/editEmployeeRecords.html')
            # return HttpResponseRedirect(reverse('adminSHS:editEmployeeRecords', args=[id]))

class deleteEmployeeRecord(View):
    def get(self, request, id):
        print('yes')
        try:
            id = signing.loads(id)
            employee = EmployeeDetails.objects.get(employee_id=id)
            user = User.objects.get(id=id)
            employee.delete()
            user.delete()
            logger.info('Record deleted')
        except:
            print('Error')
        finally:
            return redirect('/adminSHS/editEmployeeRecords.html')
    
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
            return redirect('/adminSHS/appointmentTransactionRequests.html')
    
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
            return redirect('/adminSHS/insuranceTransactionRequests.html') 

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