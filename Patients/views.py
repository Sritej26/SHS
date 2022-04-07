from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from HospitalStaff.models import AppointmentDetails
from InsuranceStaff.models import InsuranceClaimDetails
from InsuranceStaff.models import InsurancePolicies
from InsuranceStaff.models import InsuranceClaimRegister
from .forms import *
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import * 
from Hospitalportal.models import * 
from django.views.decorators.cache import cache_control
import logging
from datetime import datetime
from Doctors.models import *
from django.core import signing
import uuid
from HospitalStaff.helper import mask,unmask


logging.basicConfig(filename="userstatus.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()

logger.setLevel(logging.INFO)
def logout_user(request,id):
    id = signing.loads(id)
    logout(request)
    print("Loggedout")
    username= PatientDetails.objects.get(patient_id=id)
    test = HospitalPortal.objects.get(username=username.patient_name)
    test.session='N'
    test.save()
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    #logger.info("USERNAME:  " username.patient_name "   LOGOUTIME:   "+dt_string)
    return redirect('/Login')

class patientHome(View):
     def get(self,request,id):     
        id = signing.loads(id)   
        if not (request.user.is_authenticated):
            return redirect('/Login')
            docObj = DoctorDetails(doctor_id=3,doctor_name="Dr.Prem",doctor_spec="General Appointment",
                                               slot=20)
            docObj.save()
          # print(user.is_authenticated)
          # print(request.session .get('id'))
         # print(request.id)
          # id = signing.loads(id)
          
        noOfAppointments = AppointmentDetails.objects.filter(patient_id=id,status ="Confirmed").count()
        noOfLabRequestsPending = labTests.objects.filter(patient_id=id ,lab_test_status="adding....").count()
         
        homeInfo={'noOfAppointments':noOfAppointments,'noOfLabRequestsPending':noOfLabRequestsPending,'Member Since' :5}
        return render(request,'patientHome.html',{
            'id':id,
            'homeInfo' : homeInfo
         })
 

class bookAppointment(View):
    def get(self,request,id):
       if not (request.user.is_authenticated):
            return redirect('/Login') 
       id = signing.loads(id)
       docDetails = DoctorDetails.objects.all()
       appDetail = AppointmentDetails.objects.filter(patient_id=id)
       record =[]
       for detail in appDetail:
            docDetail = DoctorDetails.objects.get(doctor_id =detail.doctor_id)
            data = {'appointment_id': detail.appointment_id,'first_name': detail.first_name,'last_name': detail.last_name,
            'doctor_name': docDetail.doctor_name,'doctor_spec': docDetail.doctor_spec,'requested_date': detail.requested_date,'status':detail.status}
            record.append(data)

       return render(request,'bookAppointment.html',{
            'user':'aish',
            'appointmentForm': appointmentForm,
            'record': record,
            'id':id,
            'docDetails': docDetails,
        })
    def post(self,request,id):
        msgS = ''
        msgE=[]
        error=0
        try:
            form = appointmentForm(request.POST)
            id = signing.loads(id)
            if form.is_valid():
                doc_id_list = []
                first_name = form.cleaned_data.get('first_name')
                last_name = form.cleaned_data.get('last_name')
                requested_date = form.cleaned_data.get('requested_date')
                
                docs = DoctorDetails.objects.all()

                for i in docs :
                     doc_id_list.append(i.doctor_id)  
 

                if not request.POST.get('first_name'):
                     msgE.append( "First Name is Mandatory")
                     error=error+1
                if not request.POST.get('last_name'):
                     msgE.append( "Last Name is Mandatory")
                     error=error+1
                if not request.POST.get('requested_date'):
                    msgE.append( "Requested Date is Mandatory")
                    error=error+1
                 
                if request.POST.get('doctor_id'):
                    doctor_id=signing.loads(request.POST.get('doctor_id')   )
                    if int(doctor_id) not in doc_id_list :
                        msgE.append("Invalid Doctor Selection")
                        error=error+1
                else :
                    msgE.append("Selecting a Doctor is Mandatory")
                    error = error + 1
                if(error>=1):
                    exit()

                AppointmentObj = AppointmentDetails(patient_id=id,first_name=first_name,last_name=last_name,
                                             doctor_id=doctor_id,requested_date=requested_date)
                print("3")
                AppointmentObj.save()
                print("Saved")
                msgS = "Added Successfully"
            else:
                msgE = "Enter Valid Inputs"
        except:
            print("in except block")
            msgE = msgE
            exit()
        finally:
            id = signing.dumps(id)
            print("in finally block")
            messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR,
                                 (msgS if not msgS == '' else msgE),
                                 extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
            return HttpResponseRedirect(reverse('patient:bookAppointment', args=[id]))


class updateAppointment(View):
    def get(self, request,a_id,id):
        try:
            if not (request.user.is_authenticated):
                 return redirect('/Login')
            a_id = signing.loads(a_id)
            id = signing.loads(id)
            docDetails = DoctorDetails.objects.all()
            detail = AppointmentDetails.objects.get(appointment_id=a_id)
            docDetail = DoctorDetails.objects.get(doctor_id =detail.doctor_id)
             
            detail = {'appointment_id': detail.appointment_id,'patient_id': detail.patient_id,'first_name': detail.first_name,'last_name': detail.last_name,
                        'doctor_id': detail.doctor_id,'requested_date': detail.requested_date}
        finally:
            return render(request, 'updateAppointment.html', {               
               'appointmentForm': appointmentForm(detail),   
               'id':id, 
               'docDetail':docDetail,
               'docDetails':docDetails              
            })
    def post(self, request,a_id, id):
        msgS=''
        error = 0
        msgE=[]
        try:
            # try:
            #     id = signing.loads(id)
            # except:
            #     raise Http404
            a_id = signing.loads(a_id)
            id = signing.loads(id)
            detail = AppointmentDetails.objects.get(appointment_id=a_id)
                        # client_persons=client_person.objects.filter(client_id=id)
            detailForm = appointmentForm(request.POST)
            if detailForm.is_valid():
                detail.first_name = detailForm.cleaned_data.get('first_name')
                detail.last_name = detailForm.cleaned_data.get('last_name')
             
                # detail.doctor_id = request.POST.get('doctor_id')
                detail.requested_date = detailForm.cleaned_data.get('requested_date')

                if not request.POST.get('first_name'):
                    print("In exception !!!!!!!!!!!!!")
                    msgE.append( "First Name is Mandatory")
                    error=error+1
                if not request.POST.get('last_name'):
                    msgE.append( "Last Name is Mandatory")
                    error=error+1
                if not request.POST.get('requested_date'):
                    msgE.append( "Requested Date is Mandatory")
                    error=error+1


                doc_id_list =[]
                docs = DoctorDetails.objects.all()
                for i in docs :
                    doc_id_list.append(i.doctor_id)  


                if request.POST.get('doctor_id'):
                    doctor_id=signing.loads(request.POST.get('doctor_id')   )
                    if int(doctor_id) not in doc_id_list :
                        msgE.append("Invalid Doctor Selection")
                        error=error+1
                else :
                    msgE.append("Selecting a Doctor is Mandatory")
                    error = error + 1
                if(error>=1):
                    exit()
                
                detail.doctor_id = doctor_id
                detail.save()
            msgS="Updated Successfully"
        except:
            print("in except block")
            msgE = msgE
            exit()
        finally:
            id = signing.dumps(id)
            a_id = signing.dumps(a_id)
            messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR, (msgS if not msgS == '' else msgE),
                                 extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
            return HttpResponseRedirect(reverse('patient:updateAppointment', args=[a_id,id] ))

class insuranceClaimRequest(View):
    def get(self,request,id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        id = signing.loads(id)
        appDetails = InsuranceClaimDetails.objects.filter(patient_id=id)
        policyDetails = InsurancePolicies.objects.all()
        return render(request,'insuranceClaimRequest.html',{
            'user':'aish',
            'insuranceClaimRequestForm': insuranceClaimRequestForm,
            'newInsurancePolicyForm':newInsurancePolicyForm,
            'appDetails': appDetails,
            'policyDetails': policyDetails,
            'id':id,
           
        })
    def post(self,request,id):
        msgS = ''
        try:
            form = insuranceClaimRequestForm(request.POST)
            id = signing.loads(id)
            if form.is_valid():
                patient_firstname = form.cleaned_data.get('patient_firstname')
                patient_lastname = form.cleaned_data.get('patient_lastname')
                policy_name = request.POST.get('policy_name')
                print(policy_name)
                claim_amt = form.cleaned_data.get('claim_amt')
                print("going to save")
                InsuranceClaimObj = InsuranceClaimDetails(patient_id=id,patient_firstname=patient_firstname,patient_lastname=patient_lastname,
                                            policy_name=policy_name,claim_amt=claim_amt)
                InsuranceClaimObj.save()
                print("Saved")
                msgS = "Added Successfully"
            else:
                msgE = "Mention Name of the Application Type"
        except:
            print("in except block")
            msgE = "Something went Wrong"
        finally:
            print("in finally block")
            id = signing.dumps(id)
            messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR,
                                 (msgS if not msgS == '' else msgE),
                                 extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
            return HttpResponseRedirect(reverse('patient:insuranceClaimRequest', args=[id]))


class updateInsuranceClaimRequest(View):
  
    def get(self, request, claim_id,id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        try:
            detail = InsuranceClaimDetails.objects.get(claim_id=claim_id)
            detail = {'patient_id': detail.patient_id,'patient_firstname': detail.patient_firstname,'patient_lastname': detail.patient_lastname,
                        'policy_name': detail.policy_name,'claim_amt': detail.claim_amt}
        finally:
            return render(request, 'updateInsuranceClaimRequest.html', {               
                'insuranceClaimRequestForm': insuranceClaimRequestForm(detail), 
                'id':id,    
                'claim_id':claim_id               
            })
    def post(self, request, claim_id,id):
        msgS=''
        try:
            # try:
            #     id = signing.loads(id)
            # except:
            #     raise Http404
            detail = InsuranceClaimDetails.objects.get(claim_id=claim_id)
            # client_persons=client_person.objects.filter(client_id=id)
            detailForm = insuranceClaimRequestForm(request.POST)
            if detailForm.is_valid():
                # detail.first_name = escapeXSS(str(request.POST.get('first_name')))
                # detail.first_name = escapeXSS(str(request.POST.get('address')))
                # detail.first_name = signing.loads(request.POST.get('sector'))
                # detail.first_name = signing.loads(request.POST.get('under_ministry'))
                detail.patient_firstname = request.POST.get('patient_firstname')
                detail.patient_lastname = request.POST.get('patient_lastname')
                #detail.policy_name = request.POST.get('policy_name')
                detail.claim_amt = request.POST.get('claim_amt')
                detail.save()
            msgS="Updated Successfully"
        except:
            msgE="Something Went Wrong"
        finally:
            # id = signing.dumps(id)
            messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR, (msgS if not msgS == '' else msgE),
                                 extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
            return HttpResponseRedirect(reverse('patient:updateInsuranceClaimRequest', args=[claim_id,id]))
 

class nextAppointment(View):
     def get(self, request, id):
         try:
             detail = AppointmentDetails.objects.get(appointment_id=id)
             detail = {'appointment_id': detail.appointment_id,'patient_id': detail.patient_id,'first_name': detail.first_name,'last_name': detail.last_name,
                         'doctor_id': detail.doctor_id}
         finally:
             return render(request, 'bookAppointment.html', {               
                 'appointmentForm': appointmentForm(detail),             
             })
     def post(self,request, id):
         msgS = ''
         try:
             form = appointmentForm(request.POST)
             if form.is_valid():
                 first_name = form.cleaned_data.get('first_name')
                 last_name = form.cleaned_data.get('last_name')
                 requested_date = form.cleaned_data.get('requested_date')
                 doctor_id = form.cleaned_data.get('doctor_id')
                 print("going to save")
                 AppointmentObj = AppointmentDetails(patient_id=2,first_name=first_name,last_name=last_name,
                                             doctor_id=doctor_id,requested_date=requested_date)
                 AppointmentObj.save()
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
             return redirect('/patient/bookAppointment')

class registerPolicy(View):
    
    def get(self,request,policy_id,id):
        if not (request.user.is_authenticated):
                 return redirect('/Login')
        
        appDetails = InsuranceClaimRegister.objects.all()
        policyDetails = InsurancePolicies.objects.all()
        policy_id = signing.loads(policy_id)
        id = signing.loads(id)
        return render(request,'registerPolicy.html',{
             'user':'aish',
             'registerPolicyForm': registerPolicyForm,
             'appDetails': appDetails,
             'policyDetails': policyDetails,
            'id':id
         })
    
    def post(self,request,policy_id,id):
         msgS = ''
         msgE = ''
         form = registerPolicyForm(request.POST)  
         policy_id = signing.loads(policy_id)   
         id = signing.loads(id)
           
         request_failed = 0
         if form.is_valid():
             patient_firstname = form.cleaned_data.get('patient_firstname')
             patient_lastname = form.cleaned_data.get('patient_lastname')
             patient_age = form.cleaned_data.get('patient_age')
             patient_address = form.cleaned_data.get('patient_address')
             patient_phone_no = form.cleaned_data.get('patient_phone_no')
             patient_email = form.cleaned_data.get('patient_email')
         
             appDetails = InsuranceClaimRegister.objects.filter(patient_id=4)
 
             for i in appDetails: 
                 if (i.patient_firstname.casefold() == patient_firstname.casefold() and 
                     i.patient_lastname.casefold() == patient_lastname.casefold() and 
                     i.policy_id == int(id) and i.patient_id == id):
                     request_failed = 1
                     msgE = "Already Registered"
             if request_failed == 0:
                 print("going to save")
                 InsuranceClaimRegisterObj = InsuranceClaimRegister(patient_id = id,patient_firstname=patient_firstname,patient_lastname=patient_lastname,
                                             policy_id=policy_id,patient_age=patient_age,patient_address=patient_address,patient_phone_no=patient_phone_no,patient_email=patient_email)
                 InsuranceClaimRegisterObj.save()
                 print("Saved")
                 msgS = "Added Successfully"
         policy_id = signing.dumps(policy_id)  
         id = signing.dumps(id)
        
         messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR, (msgS if not msgS == '' else msgE),
                                 extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
         return HttpResponseRedirect(reverse('patient:registerPolicy', args=[policy_id,id]))
 
 
class patientPayment(View):
    def get(self,request,id):
          appDetails = AppointmentDetails.objects.filter(patient_id = id)
          detail = InsuranceClaimDetails.objects.filter(patient_id = id)
          return render(request,'patientPayment.html',{
              'user':'aish',
              'appDetails': appDetails,
              'detail':detail,
              'id':id
          })
   
class declineTransaction(View):
    def get(self,request,id):
        detail = AppointmentDetails.objects.get(appointment_id=id)
        detail.transaction_status = 'Declined'
        detail.save()
      
        print("Saved")
       
        messages.error(request, 'Transaction request has been declined')
        return HttpResponseRedirect(reverse('patient:bookAppointment', args=[detail.patient_id]))
        '''
        appDetails = AppointmentDetails.objects.all()
        return render(request,'bookAppointment.html',{
            'user':'aish',
            'appointmentForm': appointmentForm,
            'appDetails': appDetails,
        })
        '''

class approveTransaction(View):
    def get(self,request,id):
        detail = AppointmentDetails.objects.get(appointment_id=id)
        detail.transaction_status = 'Approved'
        detail.transaction_id ='#C{}'.format(uuid.uuid1().time_low)
        detail.save()
        print("Saved")
       
        messages.success(request, 'Transaction request has been Approved')
        return HttpResponseRedirect(reverse('patient:bookAppointment', args=[detail.patient_id]))
       
        '''
        appDetails = AppointmentDetails.objects.all()
        return render(request,'bookAppointment.html',{
            'user':'aish',
            'appointmentForm': appointmentForm,
            'appDetails': appDetails,
        })

        '''
class requestLabTests(View):
      def get(self, request, id):
          try:
              if not (request.user.is_authenticated):
                return redirect('/Login')
              id = signing.loads(id)
              testDetails = labTests.objects.filter(patient_id=id ,lab_test_status="adding....")
              testRequestRecord =[]
              for detail in testDetails:
                 docDetail = DoctorDetails.objects.get(doctor_id =detail.doctor_id)
                 data = {'test_id':detail.id,'appointment_id': detail.appointment_id,'first_name': detail.first_name,'last_name': detail.last_name,
                         'doctor_name': docDetail.doctor_name, 'lab_test':detail.lab_test, 'lab_test_status':detail.lab_test_status}
                 testRequestRecord.append(data)
              
             #  docDetail = DoctorDetails.objects.get(doctor_id =testDetails.doctor_id)
              reportDetails = labTests.objects.filter(patient_id=id, lab_test_status = "Pending")
              reportDetailsRecord = []
              for detail in reportDetails:
                 docDetail = DoctorDetails.objects.get(doctor_id =detail.doctor_id)
                 data = {'appointment_id': detail.appointment_id,'first_name': detail.first_name,'last_name': detail.last_name,
                         'doctor_name': docDetail.doctor_name, 'lab_test':detail.lab_test,
                          'lab_report_status':detail.lab_report_status,'lab_report':detail.lab_report}
                 reportDetailsRecord.append(data)
                  
              
             
          finally:
              return render(request, 'requestLabTests.html', {
                  'testRequestRecord':testRequestRecord,          
                  'reportDetails':reportDetails,
                  'id':id,
                  # 'appointmentForm': appointmentForm(detail),             
              })
      def post(self, request, id):
          print("Postttt")
          msgS='Entered'
          try:
              id = signing.loads(id)
              detail = labTests.objects.get(id=request.POST['appointment_id_value'])
              print(detail.lab_test_status)
             
              detail.lab_test_status = "Pending"
            
              detail.save()
              msgS="Updated Successfully"
          except:
              msgE="Something Went Wrong"
          finally:
              id = signing.dumps(id)
              messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR, (msgS if not msgS == '' else msgE),
                                   extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
              return HttpResponseRedirect(reverse('patient:requestLabTests', args=[id]))
  
class viewRecords(View):
     def get(self, request, id):
         try:
             if not (request.user.is_authenticated):
                return redirect('/Login')
             id = signing.loads(id)
             appDetail = AppointmentDetails.objects.filter(patient_id=id)
             record =[]
             for detail in appDetail:
                 if(detail.status == "Confirmed"):
                     print(detail.appointment_id)
                     docDetail = DoctorDetails.objects.get(doctor_id =detail.doctor_id)
                     prespDetail = prescriptions.objects.filter(appointment_id =detail.appointment_id)
                     print(prespDetail.exists())
                 
                     if(prespDetail.exists()):
 
                         data = {'appointment_id': detail.appointment_id,'first_name': detail.first_name,'last_name': detail.last_name,
                         'doctor_name': docDetail.doctor_name,'doctor_spec':docDetail.doctor_spec,'requested_date':detail.requested_date,'patient_diagnosis': detail.patient_diagnosis,'patient_diagnosis': detail.patient_diagnosis,
                         'drug': prespDetail[0].drug,'unit': prespDetail[0].unit,'dosage': prespDetail[0].dosage,'prescription_text': prespDetail[0].prescription_text}
                     else:
                         data = {'appointment_id': detail.appointment_id,'first_name': detail.first_name,'last_name': detail.last_name,
                         'doctor_name': docDetail.doctor_name,'doctor_spec':docDetail.doctor_spec,'requested_date':detail.requested_date,'patient_diagnosis': detail.patient_diagnosis,'patient_diagnosis': detail.patient_diagnosis,
                         'drug': "Not metioned",'unit': "Not mentioned",'dosage': "not mentioned",'prescription_text': "not mentioned"}
                     record.append(data)
         
         finally:
             return render(request, 'viewRecords.html', {
                 'record':record,          
                 'id':id           
             })
 
 
class viewPrescription(View):
     def get(self, request,a_id, id):
         try:
             if not (request.user.is_authenticated):
                return redirect('/Login')
             id = signing.loads(id)
             a_id = signing.loads(a_id)
             prespDetail = prescriptions.objects.get(appointment_id=a_id)
                 
         finally:
             return render(request, 'viewPrescription.html', {
                 'prespDetail':prespDetail,          
                 'id':id           
             })
 
class cancelAppointment(View):
     def get(self, request, a_id,id):
         try:
             if not (request.user.is_authenticated):
                 return redirect('/Login')
             id = signing.loads(id)
             a_id = signing.loads(a_id)
             print("About to cancel")
             detail = AppointmentDetails.objects.get(appointment_id=a_id)
              
            
             detail.status = "Cancelled"
             detail.save()
             detail = {'appointment_id': detail.appointment_id,'patient_id': detail.patient_id,'first_name': detail.first_name,'last_name': detail.last_name,
                         'doctor_id': detail.doctor_id,'requested_date': detail.requested_date}
         finally: 
              id = signing.dumps(id)
              return HttpResponseRedirect(reverse('patient:bookAppointment', args=[id]))
 
 
 
class profileUpdateRequest(View):
     def get(self,request,id):
         if not (request.user.is_authenticated):
            return redirect('/Login')
         id = signing.loads(id)
         patientDetails = PatientDetails.objects.get(patient_id =id)
         # requestDetailsConfirmed = PatientDetails.objects.filter(patient_id =id,change_request_status =2)
         # appDetail = AppointmentDetails.objects.filter(patient_id=id)
        
         return render(request,'profileUpdateRequest.html',{
             'id':id,
             'patientDetails': patientDetails,
           
          
         })
     def post(self,request,id):
         msgS = ''
         try:
             id = signing.loads(id)
             patientDetails = PatientDetails.objects.get(patient_id =id)
             print(patientDetails.patient_name)
             request_info=request.POST.get('request_info')
             patientDetails.request_info = request_info
             patientDetails.change_request_status = 1
             patientDetails.save()
             print("Saved")
             msgS = "Requested Successfully"
            
         except:
             print("in except block")
             msgE = "Something went Wrong"
         finally:
             print("in finally block")
             id = signing.dumps(id)
             messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR,
                                  (msgS if not msgS == '' else msgE),
                                  extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
             return HttpResponseRedirect(reverse('patient:profileUpdateRequest', args=[id]))
 
 
 
class contactHelp(View):
     def get(self,request,id):
         if not (request.user.is_authenticated):
            return redirect('/Login')
         id = signing.loads(id)
         patientDetails = PatientDetails.objects.get(patient_id =id)
         # requestDetailsConfirmed = PatientDetails.objects.filter(patient_id =id,change_request_status =2)
         # appDetail = AppointmentDetails.objects.filter(patient_id=id)
        
         return render(request,'profileUpdateRequest.html',{
             'id':id,
             'patientDetails': patientDetails,
           
          
         })






            


