# from asyncio.windows_events import NULL
from distutils.log import error
from email import message
from functools import reduce
from pickle import NONE
from tokenize import Number
from urllib import request
from wsgiref.simple_server import demo_app
from xml.dom.minidom import Attr
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View

from Doctors import models
from .forms import *
from django.contrib import messages
from django.utils.decorators import method_decorator
from django.db.models import Q
import operator
from Patients.models import PatientDetails
from HospitalStaff.models import AppointmentDetails
from Doctors.models import prescriptions, labTests, DoctorDetails
import datetime
from Hospitalportal.models import *
from django.core import signing
from AdminSHS.models import EmployeeDetails
from django.contrib.auth import logout
#from HospitalStaff.helper import mask,unmask
import logging

logging.basicConfig(filename="userstatus.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()

logger.setLevel(logging.INFO)

flag = 'true'

def logout_user(request):
    print("yes")
    #print(user)
    # name = signing.loads(user)
    logout(request)
    print("Loggedout")
    username = EmployeeDetails.objects.get(employee_username=doctorName)
    test = HospitalPortal.objects.get(username = username.employee_username)
    test.session='N'
    test.save()
    # now = datetime.now()
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    #logger.info("USERNAME:  " username.patient_name "   LOGOUTIME:   "+dt_string)
    return redirect('/Login')

class doctorHome(View):
    def get(self,request,id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        id = signing.loads(id)
        username = EmployeeDetails.objects.get(employee_id=id)
        global doctorName
        user = username.employee_username
        doctorName = username.employee_username
        print("called doctor again")
        doctormap = DoctorDetails.objects.get(doctor_username=user)
        doctorId = doctormap.doctor_id
        print(doctorId)
        appDetails = AppointmentDetails.objects.filter(requested_date = datetime.date.today(), status = "Confirmed", doctor_id = doctorId)
        print(appDetails)
        print(datetime.date.today())
        date = datetime.date.today()
        return render(request,'doctorHome.html',{
            'user': doctorName,
            'appDetails': appDetails,
            'date':date
        })

class addPrescription(View):
    def get(self,request, id):
        try:
            if not (request.user.is_authenticated):
                return redirect('/Login')
            print("Entered Try")
            id = signing.loads(id)
            details = AppointmentDetails.objects.filter(appointment_id=id)
            prescriptionDetails = prescriptions.objects.filter(appointment_id = id)

            details1 = {}
            print(details)
        finally:
            return render(request, 'addPrescription.html', {"prescriptionDetails": prescriptionDetails,"patientdetails" : details, 'patientPrescriptionForm': patientPrescriptionForm(details1)})
    
    def post(self, request, id):
        msgS=''
        try:
            print("Enteredpost try")
            # try:
            #     id = signing.loads(id)
            # except:
            #     raise Http404
            id = signing.loads(id)
            detail1 = AppointmentDetails.objects.get(appointment_id = id)
            print(detail1.patient_id)
            print("user detail")
            print(detail1.patient_id)
            # client_persons=client_person.objects.filter(client_id=id)
            prescription = patientPrescriptionForm(request.POST)
            print(prescription.is_valid())
            if prescription.is_valid():
                print("entered prescription if")
                # detail.first_name = escapeXSS(str(request.POST.get('first_name')))
                # detail.first_name = escapeXSS(str(request.POST.get('address')))
                # detail.first_name = signing.loads(request.POST.get('sector'))
                # detail.first_name = signing.loads(request.POST.get('under_ministry'))
                #detail1.patient_diagnosis = request.POST.get('patient_diagnosis')
                drug1 = prescription.cleaned_data.get('drug')
                print(drug1)
                unit1 = prescription.cleaned_data.get('unit')
                print(unit1)
                dosage1 = prescription.cleaned_data.get('dosage')
                prescription_text1 = prescription.cleaned_data.get('prescription_text')
                print(prescription_text1)
                print(detail1.patient_id)
                pt = detail1.patient_id
                ap = detail1.appointment_id
                fs = detail1.first_name
                ls = detail1.last_name
                rq = detail1.requested_date
                di = detail1.doctor_id
                pd = detail1.patient_diagnosis
                prescriptionObj = prescriptions(patient_id = pt,appointment_id = ap,first_name = fs,
                last_name = ls, requested_date = rq,doctor_id = di,patient_diagnosis = pd,
                drug = drug1,unit = unit1,dosage = dosage1, prescription_text = prescription_text1)
                print(prescriptionObj)
                prescriptionObj.save()
                print(detail1)
                #PatientDetailsObj = PatientDetails(patient_id = detail.patient_id,patient_name=detail.patient_name,patient_age = detail.patient_age, patient_weight = detail.patient_weight,patient_height = detail.patient_height, patient_address = detail.patient_address, patient_phone_no = detail.patient_phone_no,patient_email =detail.patient_email,insurance_id = detail.insurance_id, patient_diagnosis = detail.patient_diagnosis,patient_reports=detail.patient_reports, patient_prescription=detail.patient_prescription)
                #PatientDetailsObj.save()
                #msgS="Updated Successfully"
                messages.success(request, 'Drug Added Successfully!')
            #return HttpResponseRedirect(reverse('doctors:updatePatientDetails', args=[detail1.patient_id]))
        except:
            #msgE="Something Went Wrong"
            messages.error(request, error)
        finally:
            
            #messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR, (msgS if not msgS == '' else msgE),
             #                    extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
            #return redirect('/doctors/patientRecords/search/', args=[detail1.patient_id])
            details = AppointmentDetails.objects.filter(appointment_id=id)
            details1 = {}
            prescriptionDetails = prescriptions.objects.filter(appointment_id = detail1.appointment_id)
            id = signing.dumps(id)
            return render(request, 'addPrescription.html',{"patientdetails" : details, 'patientPrescriptionForm': patientPrescriptionForm(details1),'prescriptionDetails': prescriptionDetails})

class viewLabReports(View):
    def get(self,request):
        if not (request.user.is_authenticated):
                return redirect('/Login')
        return render(request,'viewLabReports.html',{
            'user':doctorName,
            'flag1': 'true'
        })

class addDiagnosis(View):
    def get(self,request, id):
        flag = 'false'
        try:
            if not (request.user.is_authenticated):
                return redirect('/Login')
            print("Entered Try")
            id = signing.loads(id)
            details = AppointmentDetails.objects.get(appointment_id=id)
            #lab_tests1 = AppointmentDetails.objects.get(appointment_id = id)
            print(details)
            details2 = AppointmentDetails.objects.filter(appointment_id=id)
            details = {'patient_diagnosis': details.patient_diagnosis, 'appointment_id': id}
            #lab_tests = {'lab_tests': lab_tests1.lab_tests, 'appointment_id': id}
           # print(lab_tests)
            labTestDetails = labTests.objects.filter(appointment_id = id)
            print(labTestDetails)
            #print(lab_tests)
        finally:
            return render(request, 'patientDiagnosis.html', {'details2': details2, 'flag': flag, 'labTestDetails': labTestDetails, 'diagnosisForm': diagnosisForm(details), 'labTestsForm': labTestsForm(), 'details': details})

    def post(self, request, id):
        msgS=''
        flag = 'true'
        if request.POST.get('lab_tests') in ['Complete Blood Count','Prothrombin Time','Basic Metabolic Panel','Comprehensive Metabolic Panel','Lipid Panel','Liver Panel','Thyroid Stimulating Hormone','Hemoglobin A1C','Urinalysis']:
            print("-------")
            try:
                print("Enteredlab try")
                # try:
                #     id = signing.loads(id)
                # except:
                #     raise Http404
                id = signing.loads(id)
                detail1 = AppointmentDetails.objects.get(appointment_id = id)
                labDeatils = labTests.objects.filter(appointment_id = id)
                testNames = []
                for i in labDeatils:
                    testNames.append(i.lab_test)
                labTests1 = labTestsForm(request.POST)
                if labTests1.is_valid():
                    if labTests1.cleaned_data.get('lab_tests') in testNames:
                        return messages.error(request, labTests1.cleaned_data.get('lab_tests') + ' already recommended')
                    lab_tests1 = labTests1.cleaned_data.get('lab_tests')
                    print(lab_tests1)
                    pt = detail1.patient_id
                    ap = detail1.appointment_id
                    fs = detail1.first_name
                    ls = detail1.last_name
                    rq = detail1.requested_date
                    di = detail1.doctor_id
                    pd = detail1.patient_diagnosis

                    labTestObj = labTests(patient_id = pt,appointment_id = ap,first_name = fs,
                    last_name = ls, requested_date = rq,doctor_id = di, patient_diagnosis = pd,lab_test = lab_tests1, lab_test_status = 'Recommended',lab_report_status = True)
                    print(labTestObj)
                    labTestObj.save()
                    print(detail1)
                    messages.success(request, labTests1.cleaned_data.get('lab_tests')+' Added Successfully!')
                #return HttpResponseRedirect(reverse('doctors:updatePatientDetails', args=[detail1.patient_id]))
            except:
                #msgE="Something Went Wrong"
                messages.error(request, error)
            finally:
               
                #messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR, (msgS if not msgS == '' else msgE),
                    #                    extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
                #return redirect('/doctors/patientRecords/search/', args=[detail1.patient_id])
                details = AppointmentDetails.objects.get(appointment_id=id)
                #lab_tests1 = AppointmentDetails.objects.get(appointment_id = id)
                print(details)
                details = {'patient_diagnosis': details.patient_diagnosis, 'appointment_id': id}
                #lab_tests = {'lab_tests': lab_tests1.lab_tests, 'appointment_id': id}
                labTestDetails = labTests.objects.filter(appointment_id = id)
                print(labTestDetails)
                details2 = AppointmentDetails.objects.filter(appointment_id=id)
                id = signing.dumps(id)
                return render(request, 'patientDiagnosis.html', {'details2':details2,'flag': flag,'labTestDetails': labTestDetails, 'diagnosisForm': diagnosisForm(details), 'labTestsForm': labTestsForm(), 'details': details})

        else:
            try:
                print("Eneubhjd")
                print("Enteredpost try")
                # try:
                #     id = signing.loads(id)
                # except:
                #     raise Http404
                id = signing.loads(id)
                detail1 = AppointmentDetails.objects.get(appointment_id = id)
                print(detail1.patient_id)
                print("user detail")
                print(detail1.patient_id)
                # client_persons=client_person.objects.filter(client_id=id)
                diagnosis = diagnosisForm(request.POST)
                print(diagnosis.is_valid())
                if diagnosis.is_valid():
                    print("entered if")
                    # detail.first_name = escapeXSS(str(request.POST.get('first_name')))
                    # detail.first_name = escapeXSS(str(request.POST.get('address')))
                    # detail.first_name = signing.loads(request.POST.get('sector'))
                    # detail.first_name = signing.loads(request.POST.get('under_ministry'))
                    detail1.patient_diagnosis = request.POST.get('patient_diagnosis')
                    detail1.save()
                    print(detail1)
                    #PatientDetailsObj = PatientDetails(patient_id = detail.patient_id,patient_name=detail.patient_name,patient_age = detail.patient_age, patient_weight = detail.patient_weight,patient_height = detail.patient_height, patient_address = detail.patient_address, patient_phone_no = detail.patient_phone_no,patient_email =detail.patient_email,insurance_id = detail.insurance_id, patient_diagnosis = detail.patient_diagnosis,patient_reports=detail.patient_reports, patient_prescription=detail.patient_prescription)
                    #PatientDetailsObj.save()
                    #msgS="Updated Successfully"
                    messages.success(request, 'Patient Diagnosis Added Successfully!')
                #return HttpResponseRedirect(reverse('doctors:updatePatientDetails', args=[detail1.patient_id]))
            except:
                #msgE="Something Went Wrong"
                messages.error(request, 'Something Went Wrong!')
            finally:
               
                #messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR, (msgS if not msgS == '' else msgE),
                #                    extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
                #return redirect('/doctors/patientRecords/search/', args=[detail1.patient_id])
                details = AppointmentDetails.objects.get(appointment_id=id)
                #lab_tests1 = AppointmentDetails.objects.get(appointment_id = id)
                details2 = AppointmentDetails.objects.filter(appointment_id=id)
                print(details)
                details = {'patient_diagnosis': details.patient_diagnosis, 'appointment_id': id}
                #lab_tests = {'lab_tests': lab_tests1.lab_tests, 'appointment_id': id}
                labTestDetails = labTests.objects.filter(appointment_id = id)
                id = signing.dumps(id)
                return render(request, 'patientDiagnosis.html', {'details2':details2,'flag': flag,'labTestDetails': labTestDetails, 'diagnosisForm': diagnosisForm(details), 'labTestsForm': labTestsForm(), 'details': details})

class patientRecords(View):
    def get(self,request):
        if not (request.user.is_authenticated):
                return redirect('/Login')
        return render(request,'patientRecords.html',{
            'user':doctorName
        })

class patientDiagnosis(View):
    def get(self,request):
        if not (request.user.is_authenticated):
                return redirect('/Login')
        return render(request,'searchDiagnosis.html',{
            'user':doctorName
        })

def searchBar(request):
    flag = "true"
    flag1 = "true"
    if request.method == 'GET':
        if not (request.user.is_authenticated):
                return redirect('/Login')
        query = request.GET.get('query')
        patientid = PatientDetails.objects.all()
        patientdetails = PatientDetails.objects.filter(patient_id = query)
        if query and patientdetails:
            print("search bar")
            print(patientdetails)
            details = {}
            return render(request, 'searchResultsView.html', {'patientdetails': patientdetails, "details": details, "flag1": flag1, "flag":flag})
        else:
            flag1 = "false"
            print("No patient with this id number")
            #messages.error(request, 'No patient with this id number')
            return render(request, 'searchResultsView.html',{"flag1":flag1, "flag":flag})

def searchLabReports(request):
    flag1 = "true"
    if request.method == 'GET':
        if not (request.user.is_authenticated):
                return redirect('/Login')
        query = request.GET.get('query')
        #query1 = request.GET.get('query1')
        labreportdetails = labTests.objects.filter(appointment_id = query)
        if query and labreportdetails:
            #labreportdetails = labreportdetails.filter(lab_Tests = query1)
            print("search bar")
            print("labreportdetails")
            print(labreportdetails)
            details = {}
            return render(request, 'viewLabReports.html', {'labreportdetails': labreportdetails, "details": details,"flag1":flag1})
        else:
            flag1 = "false"
            return render(request, 'viewLabReports.html',{"flag1":flag1})

def searchDiagnosis(request):
    flag = "true"
    flag1 = "true"
    if request.method == 'GET':
        if not (request.user.is_authenticated):
                return redirect('/Login')
        print("Entered Serach Diagnosis")
        query = request.GET.get('query')
        patientdetails = AppointmentDetails.objects.filter(patient_id = query)
        if query and patientdetails:
            #patientdetails = patientdetails.filter(doctor_id = 2)
            print("search bar")
            print(patientdetails)
            details = {}
            return render(request, 'ViewDiagnosis.html', {'patientdetails': patientdetails, "details": details,"flag1":flag1, "flag":flag})
        else:
            flag1 = "false"
            flag = "true"
            return render(request, 'ViewDiagnosis.html',{"flag1":flag1, "flag":flag})

def searchAppointments(request):
    if request.method == 'GET':
        if not (request.user.is_authenticated):
                return redirect('/Login')
        print(request)
        print("Entered search")
        doctormap = DoctorDetails.objects.get(doctor_username=doctorName)
        print("Docto mao")
        print(doctormap)
        doctorId = doctormap.doctor_id
        print(doctorId)
        start = request.GET.get('start')
        appDetails = AppointmentDetails.objects.filter(requested_date = start, status = "Confirmed", doctor_id = doctorId)
        date = start
        return render(request,'doctorHome.html',{
            'user':doctorName,
            'appDetails': appDetails,
            'date': date
        })

class updatePatientDetails(View):
    def get(self, request, id):
        flag = 'false'
        try:
            print("entered update")
            if not (request.user.is_authenticated):
                return redirect('/Login')
            print("Entered try")
            id = signing.loads(id)
            details = PatientDetails.objects.get(patient_id=id)
            print(details)
            details = {'patient_id': details.patient_id,'patient_name': details.patient_name,'patient_age': details.patient_age, 'patient_weight': details.patient_weight,
            'patient_height': details.patient_height, 'patient_address': details.patient_address, 'patient_phone_no': details.patient_phone_no,
            'patient_email': details.patient_email}
            print(details)
        finally:
            print("enteed finally")
            return render(request, 'searchResultsView.html', {'details': details, 'patientDetailsForm': patientDetailsForm(details), "flag":flag})
    
    def post(self, request, id):
        msgS=''
        try:
            print("Enteredpost try")
            # try:
            #     id = signing.loads(id)
            # except:
            #     raise Http404
            id = signing.loads(id)
            detail1 = PatientDetails.objects.get(patient_id = id)
            print(detail1.patient_id)
            print("user detail")
            print(detail1.patient_id)
            # client_persons=client_person.objects.filter(client_id=id)
            detailForm = patientDetailsForm(request.POST)
            print(detailForm.is_valid())
            if detailForm.is_valid():
                print("entered if")
                # detail.first_name = escapeXSS(str(request.POST.get('first_name')))
                # detail.first_name = escapeXSS(str(request.POST.get('address')))
                # detail.first_name = signing.loads(request.POST.get('sector'))
                # detail.first_name = signing.loads(request.POST.get('under_ministry'))
                detail1.patient_id = request.POST.get('patient_id')
                detail1.patient_name = request.POST.get('patient_name')
                detail1.patient_age = request.POST.get('patient_age')
                detail1.patient_weight = request.POST.get('patient_weight')
                detail1.patient_height = request.POST.get('patient_height')
                detail1.patient_address = request.POST.get('patient_address')
                detail1.patient_phone_no = request.POST.get('patient_phone_no')
                detail1.patient_email = request.POST.get('patient_email')
                detail1.save()
                print(detail1.patient_id)
                #PatientDetailsObj = PatientDetails(patient_id = detail.patient_id,patient_name=detail.patient_name,patient_age = detail.patient_age, patient_weight = detail.patient_weight,patient_height = detail.patient_height, patient_address = detail.patient_address, patient_phone_no = detail.patient_phone_no,patient_email =detail.patient_email,insurance_id = detail.insurance_id, patient_diagnosis = detail.patient_diagnosis,patient_reports=detail.patient_reports, patient_prescription=detail.patient_prescription)
                #PatientDetailsObj.save()
                #msgS="Updated Successfully"
                messages.success(request, 'Patient Details Updated Successfully!')
            #return HttpResponseRedirect(reverse('doctors:updatePatientDetails', args=[detail1.patient_id]))
        except:
            #msgE="Something Went Wrong"
            messages.error(request, 'Something Went Wrong!')
        finally:
        
            #messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR, (msgS if not msgS == '' else msgE),
             #                    extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
            flag = 'true'
            flag1 = 'true'
            #return redirect('/doctors/patientRecords/search/', args=[detail1.patient_id])
            print(detail1.patient_id)
            patientdetails = PatientDetails.objects.filter(patient_id = detail1.patient_id)
            print(patientdetails)
            id = signing.dumps(id)
            return render(request, 'searchResultsView.html',{"flag1": flag1, "patientdetails":patientdetails, "flag":flag})


class updatePatientDiagnosis(View):
    def get(self, request, id):
        flag = 'false'
        try:
            if not (request.user.is_authenticated):
                return redirect('/Login')
            print("Entered try")
            print(id)
            id = signing.loads(id)
            details = AppointmentDetails.objects.get(appointment_id=id)
            print(details)
            details = {'appointment_id': details.appointment_id,'patient_id': details.patient_id,'first_name': details.first_name, 'last_name': details.last_name,
            'doctor_id': details.doctor_id, 'requested_date': details.requested_date, 'status': details.status,
            'patient_diagnosis': details.patient_diagnosis}
            print(details)
        finally:
            print("enteed finally")
            return render(request, 'ViewDiagnosis.html', {'details': details, 'patientDiagnosisForm': patientDiagnosisForm(details), "flag":flag})
    
    def post(self, request, id):
        msgS=''
        try:
            print("Enteredpost try")
            # try:
            #     id = signing.loads(id)
            # except:
            #     raise Http404
            id = signing.loads(id)
            detail1 = AppointmentDetails.objects.get(appointment_id = id)
            print(detail1.patient_id)
            print("user detail")
            print(detail1.patient_id)
            # client_persons=client_person.objects.filter(client_id=id)
            detailForm = patientDiagnosisForm(request.POST)
            print(detailForm.is_valid())
            if detailForm.is_valid():
                print("entered if")
                # detail.first_name = escapeXSS(str(request.POST.get('first_name')))
                # detail.first_name = escapeXSS(str(request.POST.get('address')))
                # detail.first_name = signing.loads(request.POST.get('sector'))
                # detail.first_name = signing.loads(request.POST.get('under_ministry'))
                detail1.patient_diagnosis = request.POST.get('patient_diagnosis')
                detail1.save()
                print(detail1.patient_id)
                #PatientDetailsObj = PatientDetails(patient_id = detail.patient_id,patient_name=detail.patient_name,patient_age = detail.patient_age, patient_weight = detail.patient_weight,patient_height = detail.patient_height, patient_address = detail.patient_address, patient_phone_no = detail.patient_phone_no,patient_email =detail.patient_email,insurance_id = detail.insurance_id, patient_diagnosis = detail.patient_diagnosis,patient_reports=detail.patient_reports, patient_prescription=detail.patient_prescription)
                #PatientDetailsObj.save()
                #msgS="Updated Successfully"
                messages.success(request, 'Patient Diagnosis Updated Successfully!')
            #return HttpResponseRedirect(reverse('doctors:updatePatientDetails', args=[detail1.patient_id]))
        except:
            #msgE="Something Went Wrong"
            messages.error(request, 'Something Went Wrong!')
        finally:
           
            #messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR, (msgS if not msgS == '' else msgE),
             #                    extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
            flag = 'true'
            flag1 = 'true'
            #return redirect('/doctors/patientRecords/search/', args=[detail1.patient_id])
            print(detail1.patient_id)
            patientdetails = AppointmentDetails.objects.filter(patient_id = request.POST.get('patient_id'))
            print(patientdetails)
            id = signing.dumps(id)
            return render(request, 'ViewDiagnosis.html',{"patientdetails":patientdetails, "flag":flag, "flag1":flag1})

class deletePatientDiagnosis(View):
    def get(self, request, id, id1):
        id1 = signing.loads(id1)
        id = signing.loads(id)
        if not (request.user.is_authenticated):
            return redirect('/Login')
        flag = "true"
        flag1 = "true"
        query = request.GET.get('query')
        patientdetails = AppointmentDetails.objects.filter(patient_id = id1)
        flag1 = "true"
        flag = "true"
        details = AppointmentDetails.objects.get(appointment_id=id)
        details.patient_diagnosis = ""
        details.save()

        return render(request, 'ViewDiagnosis.html', {'patientdetails': patientdetails, 'details': details, 'patientDiagnosisForm': patientDiagnosisForm(details),"flag1": flag1, "flag":flag})

class addnextAppointment(View):
     def get(self, request, id):
         try:
             if not (request.user.is_authenticated):
                return redirect('/Login')
             id = signing.loads(id)
             detail = AppointmentDetails.objects.get(appointment_id=id)
             detail = {'appointment_id': detail.appointment_id,'patient_id': detail.patient_id,'first_name': detail.first_name,'last_name': detail.last_name,
                         'doctor_id': detail.doctor_id}
         finally:
             return render(request, 'addnextAppointment.html', {               
                 'appointmentForm': appointmentForm(detail),             
             })
     def post(self,request, id):
         msgS = ''
         try:
             form = appointmentForm(request.POST)
             id = signing.loads(id)
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
                 msgS = "Next Appointment Added Successfully"
             else:
                 msgE = "Mention Name of the Application Type"
         except:
             print("in except block")
             msgE = "Something went Wrong"
         finally:
             
             print("in finally block")
             details = AppointmentDetails.objects.get(appointment_id=id)
             #lab_tests1 = AppointmentDetails.objects.get(appointment_id = id)
             print(details)
             details2 = AppointmentDetails.objects.filter(appointment_id=id)
             details = {'patient_diagnosis': details.patient_diagnosis, 'appointment_id': id}
             #lab_tests = {'lab_tests': lab_tests1.lab_tests, 'appointment_id': id}
            # print(lab_tests)
             labTestDetails = labTests.objects.filter(appointment_id = id)
             print(labTestDetails)
             id = signing.dumps(id)
             messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR,
                                  (msgS if not msgS == '' else msgE),
                                  extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
             return render(request, 'patientDiagnosis.html', {'details2': details2, 'flag': flag, 'labTestDetails': labTestDetails, 'diagnosisForm': diagnosisForm(details), 'labTestsForm': labTestsForm(), 'details': details})
