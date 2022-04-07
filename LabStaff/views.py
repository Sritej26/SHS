from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View
from Doctors.models import labTests
from LabStaff.models import LabReports
from HospitalStaff.models import AppointmentDetails
import json
from django.db.models import Q
from django.contrib.auth import logout
from AdminSHS.models import EmployeeDetails
from Hospitalportal.models import HospitalPortal
import logging
from django.core import signing


logging.basicConfig(filename="userstatus.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()

logger.setLevel(logging.INFO)


def logout_user(request):
    print("yes")
    #print(user)
    # name = signing.loads(user)
    logout(request)
    print("Loggedout")
    username = EmployeeDetails.objects.get(employee_username=labStaffName)
    test = HospitalPortal.objects.get(username = username.employee_username)
    test.session='N'
    test.save()
    # now = datetime.now()
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    #logger.info("USERNAME:  " username.patient_name "   LOGOUTIME:   "+dt_string)
    return redirect('/Login')
# Create your views here.
class labStaffHome(View):
    def get(self, request,id):
        #print(user)
        id = signing.loads(id)
        username = EmployeeDetails.objects.get(employee_id=id)
        global labStaffName
        labStaffName = username.employee_username

        #if not (request.user.is_authenticated):
         #   return redirect('/Login') 
        return render(request, 'labStaffHome.html', {
            'user': labStaffName
        })

class viewRequests(View):
    def get(self, request):
        #if not (request.user.is_authenticated):
         #   return redirect('/Login')
        request_details = labTests.objects.all()
        number_of_requests = len(request_details)
        return render(request, 'viewRequests.html', {
            'requests': request_details,
            'number_of_requests': number_of_requests,
            'user' : labStaffName
        })

    def post(self,request):
        msgS = ''
        try:
            request_details = labTests.objects.all()
            appoitment_id = int(request.POST.get('approve'))
            for entry in request_details:
                if entry.appointment_id == appoitment_id:
                    lab_report = LabReports(doctor_id = entry.doctor_id, patient_id = entry.patient_id, patient_diagnosis = entry.patient_diagnosis, lab_staff_id = 1, report_status = "Approved", test_name = entry.lab_test)
                    lab_report.save()
                    appointment = labTests.objects.get(appointment_id=entry.appointment_id)
                    appointment.lab_test_status = "Approved"
                    appointment.save()
                    msgS = "Added Successfully"
                    break
                else:
                    msgE = "Mention Name of the Application Type"
        except:
            print("in except block")
            msgE = "Something went Wrong"
        finally:
            print("in finally block")
            # messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR,
            #                      (msgS if not msgS == '' else msgE),
            #                      extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
            # return redirect('/labStaff/viewRequests')
            return HttpResponseRedirect(reverse('labStaff:viewRequests'))
class addLabRecord(View):
    def get(self, request):
        #if not (request.user.is_authenticated):
         #   return redirect('/Login')
        request_details = LabReports.objects.filter(report_status="Approved")
        return render(request, 'labReportPage.html', {
            'requests': request_details,
            'user' : labStaffName
        })
    def post(self,request):
        
        details = str(request.POST.get('details'))
        record_id=request.POST.get('addData')
        
        message=""
        try:
            report_data= LabReports.objects.get(id=record_id)
            report_data.report_info=details
            report_data.report_status="Added"
            report_data.save()    
            message="Added Scuccessfully"
                
        except:
            print("exception while fetching reports")
            message="Exception in fetching Lab Reports"
        finally:
            # return redirect('/labStaff/addLabRecord')
            return HttpResponseRedirect(reverse('labStaff:addLabRecord'))

            

class updateLabRecord(View):
    def get(self, request):
        #if not (request.user.is_authenticated):
         #   return redirect('/Login')
        crit=Q(report_status="Added")
        crit1=Q(report_status="Updated")
        request_details = LabReports.objects.filter(crit | crit1 )
       
        return render(request, 'updateReportPage.html', {
            'requests': request_details,
            'user' : labStaffName
        })
    def post(self,request):
        details = str(request.POST.get('details'))
        record_id=request.POST.get('update')
        message=""
        try:
            report_data= LabReports.objects.get(id=record_id)
            report_data.report_info=details
            report_data.report_status="Updated"
            report_data.save()      
            message="Updated Scuccessfully"
        except:
            print("exception while updating  reports")
            message="Exception in fetching Lab Reports"
        finally:
            return HttpResponseRedirect(reverse('labStaff:updateLabRecord'))

            # return redirect('/labStaff/updateLabRecord')


    
class viewLabRecord(View):
    def get(self, request):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        request_details = LabReports.objects.all()
        return render(request, 'viewReportPage.html', {
            'requests': request_details,
            'user' : labStaffName
        })