# -*- coding: utf-8 -*-

from django.shortcuts import render
from HospitalStaff.forms import patientDetailsForm
from Hospitalportal.models import HospitalPortal
from Patients.forms import appointmentForm
from Patients.forms import editForm
from Patients.models import PatientDetails
from django.contrib import messages
# from .forms import changeStatusform
 # Create your views here.
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from HospitalStaff.models import AppointmentDetails
#from .forms import *
from Doctors.models import DoctorDetails
from Doctors.models import prescriptions
from Doctors.models import labTests
from django.utils.decorators import method_decorator
import logging
from AdminSHS.models import EmployeeDetails
from Hospitalportal.models import *
from django.contrib.auth import logout
from datetime import datetime
from django.core import signing


logging.basicConfig(filename="userstatus.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()

logger.setLevel(logging.INFO)





class hospitalStaffHome(View):
    def get(self,request,id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        id = signing.loads(id)
        username = EmployeeDetails.objects.get(employee_id=id)
      
        global hospitalStaffName 
        hospitalStaffName = username.employee_username
        print(hospitalStaffName)
        appointments_count= AppointmentDetails.objects.all().count()
        update_req_count= PatientDetails.objects.filter(change_request_status = 1).count()
        return render(request,'staffHome.html',{
            'user':hospitalStaffName,
            'appointments_count':appointments_count,
            'update_req_count':update_req_count,
            # 'hospitalStaffName':hospitalStaffName
        })

def logout_user(request):
    logout(request)
    print("Loggedout")
    
    username = EmployeeDetails.objects.get(employee_username=hospitalStaffName)
    test = HospitalPortal.objects.get(username = username.employee_username)
    test.session='N'
    test.save()
    #staff= HospitalPortal.objects.get(username=id)
    # test = HospitalPortal.objects.get(username=username.patient_name)
   
    #now = datetime.now()
    #dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
   # logger.info("USERNAME:  "+staff.username+"   LOGOUTIME:   "+dt_string)
    return redirect('/Login')


class createRecord(View):
    def get(self, request):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        print(hospitalStaffName)
        flag = 'false'
        try:
            print("Entered try")
            #details = PatientDetails.objects.get(patient_id=id)
            details = {}
            print(details)
        finally:
            print("enteed finally")
            return render(request, 'createRecord.html', {'details': details, 'patientDetailsForm': patientDetailsForm(details), "flag":flag, 'user':hospitalStaffName})
    
    def post(self, request):
        msgS=''
        try:
            print("Entered hospital post try")
            # try:
            #     id = signing.loads(id)
            # except:
            #     raise Http404
            # client_persons=client_person.objects.filter(client_id=id)
            detailForm = patientDetailsForm(request.POST)
            if detailForm.is_valid():
                print("In post try")
                # detail.first_name = escapeXSS(str(request.POST.get('first_name')))
                # detail.first_name = escapeXSS(str(request.POST.get('address')))
                # detail.first_name = signing.loads(request.POST.get('sector'))
                # detail.first_name = signing.loads(request.POST.get('under_ministry'))
               
                patient_name = request.POST.get('patient_name')
                patient_age = request.POST.get('patient_age')
                patient_weight = request.POST.get('patient_weight')
                patient_height = request.POST.get('patient_height')
                patient_address = request.POST.get('patient_address')
                patient_phone_no = request.POST.get('patient_phone_no')
                patient_email = request.POST.get('patient_email')
                
                
                PatientDetailsObj = PatientDetails(patient_name=patient_name,patient_age = patient_age, patient_weight = patient_weight,patient_height = patient_height, patient_address = patient_address, patient_phone_no = patient_phone_no,patient_email =patient_email)
                PatientDetailsObj.save()
                messages.success(request, 'Patient details saved successfully!')
                return redirect('/hospitalStaff/createRecord')
            else:
                print('sadfghjkl')
                messages.error(request, 'Something went wrong!')
        except:
            msgE = "SomeThing"


class approveAppointment(View):
    def get(self, request):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        appDetails = AppointmentDetails.objects.all()
        

        return render(request,'approveAppointment.html',{
            'user': hospitalStaffName,
            
            'appDetails': appDetails,
            # 'hospitalStaffName':hospitalStaffName
            
        })
        
    def post(self,request):
        print("Enteredpost try")
        
        msgS = ''
        try:
            appDetails = AppointmentDetails.objects.all()
            #if status1.is_valid():
            #print('inside valid')
            update_status=request.POST.get('options')
            update_id=request.POST.get('appointment_id')
            print(update_status)
            print(update_id)
            update_appointment=AppointmentDetails.objects.get(appointment_id=update_id)
            if(update_appointment.status!='Confirmed'):
                update_appointment.status=update_status
                if(update_status=='Confirmed'):
                    update_appointment.transaction_status='Pending'
                
                update_appointment.save()
                msgS = "Status Updated Successfully"
                messages.success(request, 'Appointment Status Updated successfully!')
            elif(update_appointment.status=='Confirmed' and update_status!='Confirmed'):
                messages.error(request, 'Can\'t Update Confirmed Appointments!')
                
            
        except:
            msgE="Something went wrong"
            messages.error(request, 'Something went wrong!')
        # print(request.POST)
        
        finally:    
            # messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR,
            #                      (msgS if not msgS == '' else msgE),
            #                      extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
            
            return render(request,'approveAppointment.html',{
                'user':hospitalStaffName,
                
                'appDetails': appDetails,
                
            })
    
# class viewDetails(View):
#     def get(self, request):
        
#         appDetails = AppointmentDetails.objects.all()
        

#         return render(request,'viewDetails.html',{
#             'user':'sritej',
            
#             'appDetails': appDetails
            
#         })

class viewDetails1(View):
    def get(self, request):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        
        #appDetails = AppointmentDetails.objects.all()
        

        return render(request,'viewDetails1.html',{
            'user':hospitalStaffName ,
            'mainflag':True,
            'flag1':True,
            # 'hospitalStaffName':hospitalStaffName
            #'appDetails': appDetails
            
        })
    
def search(request):
    if not (request.user.is_authenticated):
            return redirect('/Login')
    print("In search")
    if request.method == 'GET':
        print("Entered Serach")
        query = request.GET.get('query')
        print(query)
        if query:
            try:
                print('in try')
                patientdetail = AppointmentDetails.objects.filter(appointment_id = query)
                print(patientdetail)
                print('after get')
                
                prescription= prescriptions.objects.filter(appointment_id=query)
                lab=labTests.objects.filter(appointment_id=query)
                pres=''
                la=''
                if(prescription):
                    for p in prescription:
                        if pres=='':
                            pres=p.prescription_text
                        else:
                            pres=pres+', '+p.prescription_text
                else:
                    pres='No Prescription yet'
                if(lab):
                    for l in lab:
                        if la=='':
                            la=l.lab_test
                        else:
                            la=la+', '+l.lab_test
                else:
                    la='No Lab test yet'
                
                flag1=True
                patientdetail1=' '
                if(patientdetail):

                    flag1=False
                    patientdetail1=patientdetail.get(appointment_id=query)
                else:
                    print('at msg no id')
                    messages.error(request, 'No Appointment with this ID!')
                
                print(patientdetail1)
                return render(request, 'ViewDetails1.html', {'patientdetail': patientdetail1,'mainflag':False,'flag1':flag1,'user':hospitalStaffName,'prescription':pres,'lab_test':la })
            except:
                print('in except')
                return render(request, 'ViewDetails1.html',{'mainflag':True},{'flag1':True})
        else:
            
            print("enter ID")
            return render(request, 'ViewDetails1.html',{'mainflag':True},{'flag1':True})  

class checkAppointmets(View):
    def get(self, request, id):
        try:
            if not (request.user.is_authenticated):
                return redirect('/Login')
            Details = AppointmentDetails.objects.get(appointment_id=id) 
            doctorId=Details.doctor_id
            date=Details.requested_date
            print(Details.appointment_id)
            appointments= AppointmentDetails.objects.filter(requested_date = date).filter(doctor_id=doctorId).count()
            print('count'+str(appointments))
            docDetails = DoctorDetails.objects.all()
            doc_id_list = []
            for i in docDetails :
                doc_id_list.append(i.doctor_id)
            if(doctorId in doc_id_list):
                doctor_details=DoctorDetails.objects.get(doctor_id=doctorId)
                #chnage for doctor availability
                if(appointments<doctor_details.slot):
                    print("In confirmed")
                    Details.status="Confirmed"
                    Details.transaction_status="Pending"
                    messages.success(request, 'Appointment has been Approved based on doctor availability')
                else:
                    Details.status="Cancelled"
                    messages.error(request, 'Appointment has been Cancelled due to unavailability of doctor')
            else:
                Details.status="Cancelled"
                messages.error(request, 'Doctor left Oragnization!')
            Details.save()
        except:
            messages.error(request, 'Doctor not found !')
        finally:    
            appDetails = AppointmentDetails.objects.all()

            return render(request,'approveAppointment.html',{
                'user':hospitalStaffName,
                'appDetails': appDetails,
                # 'hospitalStaffName':hospitalStaffName
            })

class transactions(View):
    def get(self, request):
        
        try:
            if not (request.user.is_authenticated):
                return redirect('/Login')
            print("Entered try")
            #details = PatientDetails.objects.get(patient_id=id)
            patientdetail = AppointmentDetails.objects.all()
        finally:
            print("enteed finally")
            return render(request, 'transactions.html', {'details': patientdetail,'user':hospitalStaffName})
class updatepersonalinfo(View):
    def get(self, request):
        # PatientDetailsObj = PatientDetails(patient_name="Jay",
        #                                      patient_age=35,patient_weight=55,patient_height=5,patient_address="sasddd",patient_phone_no=67,change_req_status=1,request_info="Change weight to 73")
        # PatientDetailsObj.save()
        try:
            if not (request.user.is_authenticated):
                return redirect('/Login')
            print("Entered try")
            details = PatientDetails.objects.filter(change_request_status=1)
            
        finally:
            print("enteed finally")
            return render(request, 'updatepersonalinfo.html', {'details': details,'user':hospitalStaffName})
class edit(View):
    def get(self, request, id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        details = PatientDetails.objects.get(patient_id=id) 
   
        d = {'patient_name': details.patient_name, 'patient_id': id,'patient_age':details.patient_age,'patient_weight':details.patient_weight,'patient_height':details.patient_height,'patient_address':details.patient_address,'patient_phone_no':details.patient_phone_no,'patient_email':details.patient_email}
        print('ID'+str(details.patient_id))

        return render(request,'edit.html',{
            'user':hospitalStaffName,
            'details': editForm(d),
            # 'hospitalStaffName':hospitalStaffName
            
        })
    def post(self, request, id):
        msgS=''
        try:
            print("Entered  post try")
           
            detail = PatientDetails.objects.get(patient_id=id)
            detailForm = editForm(request.POST)
            if detailForm.is_valid():
                
                #detail.patient_id = request.POST.get('patient_id')
                detail.patient_name = request.POST.get('patient_name')
                detail.patient_age = request.POST.get('patient_age')
                detail.patient_weight = request.POST.get('patient_weight')
                detail.patient_height = request.POST.get('patient_height')
                detail.patient_address = request.POST.get('patient_address')
                detail.patient_phone_no = request.POST.get('patient_phone_no')
                detail.patient_email = request.POST.get('patient_email')
                detail.change_req_status=2
                detail.save()
                messages.success(request, 'Patient details saved successfully!')
                return redirect('/hospitalStaff/updatepersonalinfo')
            else:
                print('sadfghjkl')
        except:
            msgE = "SomeThing"
        