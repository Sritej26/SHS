from django.http import HttpResponseRedirect,HttpResponse, HttpRequest
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views import View
from AdminSHS.models import EmployeeDetails
from Doctors.models import DoctorDetails
from HospitalStaff.models import AppointmentDetails
from InsuranceStaff.models import InsuranceClaimDetails
from LabStaff.models import LabReports
from .forms import *
from django.contrib import messages
from django.utils.decorators import method_decorator
from Patients.models import PatientDetails
from Hospitalportal.models import HospitalPortal
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str,force_str,DjangoUnicodeDecodeError
from .utils import generate_token
from django.core.mail import EmailMessage
from django.conf import settings
import threading
from django.template.loader import render_to_string
import logging
from datetime import datetime
from django.core import signing
import string
import pickle
from sklearn import preprocessing
#import pandas as pd
from django.core.mail import send_mail
from HospitalStaff.helper import mask,unmask
import re

now = datetime.now()
logging.basicConfig(filename="userstatus.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()

logger.setLevel(logging.INFO)
User = get_user_model()
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'   
def check(email):   
  
    if(re.search(regex,email)):   
        return True   
    else:   
        return False


my_model = pickle.load(open('maliciousLogin_model.pkl', 'rb'))
is_guest_login='1'
def get_predict(login_data):
    duration='0'
    protocol_type='1' 
    service = '1'
    dst_bytes='1'
    logged_in='1'
    is_host_login='1'
    if login_data.get('wsgi.multithread'):
        land='0'
        flag='1'
        urgent='1'
        same_srv_rate='1'
        srv_serror_rate='1'
    else:
        land='1'
        flag='0'
        urgent='0'
    num_root = '1'
    num_file_creations = '1'  
    num_shells='1'  
    sample = [[duration,protocol_type,service,land,1,
    dst_bytes,1,0,urgent,0,0,
    logged_in,1,1,1,num_root,
    num_file_creations,num_shells,1,1,
    is_host_login,is_guest_login,1,1,1,
    srv_serror_rate,1,1,same_srv_rate,
    1,1,1,1,
    1,0,0,
    1,1,1,1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
    1,1,1,1]]
 
    result = my_model.predict(sample).tolist()[0]
    print(result)
    return True if result == "normal" else False


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

class Login(View):
    def get(self,request):
        return render(request,'Login.html')
    def post(self,request): 
        form = Loginform(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            if not User.objects.filter(username=username).exists():
                messages.info(request,'USER DETAILS DOESNT EXIST, PLEASE REGISTER')
                return render(request,'Login.html')
            password = form.cleaned_data.get('password')
            user = authenticate(username=str(username),password=str(password))
            if user is not None:
                if user.is_superuser:
                    id = user.id
                    id = signing.dumps(id)
                    login(request,user)
                    return HttpResponseRedirect(reverse('adminSHS:adminHome', args=[id]))
                if not user.is_email_verified:
                    messages.add_message(request, messages.ERROR,'Email is not verified, please check your email inbox')
                    return render(request,'Login.html')
                test = HospitalPortal.objects.get(username=username)
                if test.session =='N' and get_predict(request.META):                    
                    login(request,user)
                    test.session = 'Y'
                    test.save()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    logger.info("USERNAME:  "+username+"   LOGINTIME:   "+dt_string)
                    if test.Role == 'Patient':
                        pid= PatientDetails.objects.get(patient_name=username)
                        id=pid.patient_id
                        id = signing.dumps(id)
                        return HttpResponseRedirect(reverse('patient:patientHome', args=[id]))

                    # elif test.Role == 'AdminSHS':
                    #     return redirect("/adminSHS/",{'name':user})
                    elif test.Role == 'Labstaff':
                        username = EmployeeDetails.objects.get(employee_username = user)
                        id = username.employee_id
                        id = signing.dumps(id)
                        return HttpResponseRedirect(reverse('labStaff:labStaffHome', args=[id]))
                    elif test.Role == 'Doctor':
                        username = EmployeeDetails.objects.get(employee_username = user)
                        id = username.employee_id
                        id = signing.dumps(id)
                        return HttpResponseRedirect(reverse('doctors:doctorHome', args=[id]))
                    elif test.Role == 'Insurancestaff':
                        username = EmployeeDetails.objects.get(employee_username = user)
                        id = username.employee_id
                        id = signing.dumps(id)
                        return HttpResponseRedirect(reverse('insuranceStaff:insuranceHome', args=[id]))
                    elif test.Role == 'Hospitalstaff':
                        username = EmployeeDetails.objects.get(employee_username = user)
                        id = username.employee_id
                        id = signing.dumps(id)
                        return HttpResponseRedirect(reverse('hospitalStaff:hospitalStaffHome', args=[id]))

                        
                        #return redirect("/hospitalStaff/", {'name': user})
                else:
                    messages.info(request,'User already logged in')
                    return render(request,'Login.html')  
            else:
                messages.info(request,'INVALID CREDENTIALS')
                return render(request,'Login.html')
        else:
            msgE = "Mention Name of the Application Type"    
class Registercheck(View):
    def post(self,request):
        form = Registerform(request.POST)
        if form.is_valid():
            patient_name = form.cleaned_data.get('patient_name')
            patient_age = form.cleaned_data.get('patient_age')
            patient_weight = form.cleaned_data.get('patient_weight')
            patient_height = form.cleaned_data.get('patient_height')
            patient_address = form.cleaned_data.get('patient_address')
            patient_phone_no = form.cleaned_data.get('patient_phone_no')
            patient_email = form.cleaned_data.get('patient_email')
            patient_card_details = form.cleaned_data.get('patient_card_details')
            password = form.cleaned_data.get('User_password')
            passwordcheck = form.cleaned_data.get('passwordcheck')
            if not (form.cleaned_data.get('patient_name')):
                 messages.info(request,'username mandatory')
                 return render(request,'register.html')
            if not (form.cleaned_data.get('patient_address')):
                 messages.info(request,'Address mandatory')
                 return render(request,'register.html')
            if not (form.cleaned_data.get('User_password')):
                 messages.info(request,'password mandatory')
                 return render(request,'register.html')
            if not (form.cleaned_data.get('patient_card_details')):
                 messages.info(request,'Card details mandatory')
                 return render(request,'register.html')    
            if password == passwordcheck:
                if User.objects.filter(username=patient_name).exists():
                    messages.info(request,'USER NAME ALREADY EXISTS')
                    return render(request,'register.html')
                if not check(patient_email):
                    messages.info(request,'EMAIL NOT VALID')
                    return render(request,'register.html')
                if User.objects.filter(email=str(patient_email)).exists():
                    messages.info(request,'EMAIL ALREADY EXISTS')
                    return render(request,'register.html')
                PatientDetailsObj = PatientDetails(patient_name=patient_name,patient_age = patient_age, patient_weight = patient_weight,patient_height = patient_height, patient_address = patient_address, patient_phone_no = patient_phone_no,patient_email =patient_email, card_details = patient_card_details)
                PatientDetailsObj.save()
                Userobj = User.objects.create_user(username=patient_name, password = password, email = patient_email)
                Userobj.save()
                HospitalPortalobj = HospitalPortal(username=patient_name,Role= 'Patient',session='N')
                HospitalPortalobj.save()
                send_action_email(Userobj,request)
                messages.info(request,'Please check your inbox to verify the account')
                return redirect("/Login")
            else:
                messages.info(request,'PASSWORD DIDNT MATCH')
                return render(request,'register.html')
        else:
            print("Hello")
            return render(request,'Login.html')

        
def Register(request):
    if request.method=="POST":
        return render(request,'register.html')


def activate_user(request, uidb64, token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))

        user = User.objects.get(pk=uid)

    except Exception as e:
        user = None

    if user and generate_token.check_token(user, token):
        user.is_email_verified = True
        user.save()
        if EmployeeDetails.objects.filter(employee_email = mask(user.email)).exists():
            EmployeeObject = EmployeeDetails.objects.get(employee_email = mask(user.email))
            HospitalPortalObj = HospitalPortal(Role = EmployeeObject.employee_dept, username = EmployeeObject.employee_username, session = 'N')
            HospitalPortalObj.save()
            if EmployeeObject.employee_dept == 'Doctor':
                DoctorObj = DoctorDetails(doctor_name = EmployeeObject.employee_first_name, doctor_spec = 'Physician', slot = 15, doctor_username = EmployeeObject.employee_username)
                DoctorObj.save()
        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('Login'))

    return render(request, 'activate-failed.html', {"user": user})


      