from django.http import HttpResponseRedirect,HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.views import View
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

now = datetime.now()
logging.basicConfig(filename="userstatus.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()

logger.setLevel(logging.INFO)
User = get_user_model()
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
                if not user.is_email_verified:
                    messages.add_message(request, messages.ERROR,'Email is not verified, please check your email inbox')
                    return render(request,'Login.html')
                test = HospitalPortal.objects.get(username=username)
                if test.session =='N':
                    login(request,user)
                    test.session = 'Y'
                    test.save()
                    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                    logger.info("USERNAME:  "+username+"   LOGINTIME:   "+dt_string)
                    if test.Role == 'Patient':
                        pid= PatientDetails.objects.get(patient_name=username)
                        id=pid.patient_id
                        return HttpResponseRedirect(reverse('patient:patientHome', args=[id]))

                    elif test.Role == 'Admin':
                        return redirect("/admin/",{'name':user})
                    elif test.Role == 'Labstaff':
                        return redirect("/labStaff/",{'name':user})
                    elif test.Role == 'Doctorstaff':
                        return redirect("/doctors/",{'name':user})
                    elif test.Role == 'Insurancestaff':
                        return redirect("/insurance/",{'name':user})
                    elif test.Role == 'HospitalStaff':
                        return redirect("/hospitalStaff/", {'name': user})
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
            password = form.cleaned_data.get('User_password')
            passwordcheck = form.cleaned_data.get('passwordcheck')
            if password == passwordcheck:
                if User.objects.filter(username=patient_name).exists():
                    messages.info(request,'PATIENT NAME ALREADY EXIST')
                    return render(request,'register.html')
                if User.objects.filter(email=str(patient_email)).exists():
                    messages.info(request,'EMAIL ALREADY EXIST')
                    return render(request,'register.html')
                PatientDetailsObj = PatientDetails(patient_name=patient_name,patient_age = patient_age, patient_weight = patient_weight,patient_height = patient_height, patient_address = patient_address, patient_phone_no = patient_phone_no,patient_email =patient_email)
                PatientDetailsObj.save()
                Userobj = User.objects.create_user(username=patient_name, password = password, email = patient_email)
                Userobj.save()
                HospitalPortalobj = HospitalPortal(username=patient_name,Role= 'Patient',session='N')
                HospitalPortalobj.save()
                send_action_email(Userobj,request)
                messages.info(request,'Please check your email to verify the account')
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

        messages.add_message(request, messages.SUCCESS,
                             'Email verified, you can now login')
        return redirect(reverse('Login'))

    return render(request, 'activate-failed.html', {"user": user})
