from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.shortcuts import render,redirect
from django.urls import reverse
from django.views import View
from InsuranceStaff.models import InsurancePolicies
from InsuranceStaff.models import InsuranceClaimDetails
from InsuranceStaff.models import InsuranceClaimRegister
from .forms import *
from django.contrib import messages
from django.utils.decorators import method_decorator
from AdminSHS.models import EmployeeDetails
from Hospitalportal.models import *
from django.contrib.auth import logout
import uuid
import logging
from django.core import signing

logging.basicConfig(filename="userstatus.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()

logger.setLevel(logging.INFO)
# Create your views here.
class insuranceHome(View):
    def get(self,request, id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        id = signing.loads(id)
        username = EmployeeDetails.objects.get(employee_id=id)
        
        global insuranceStaffName
        insuranceStaffName = username.employee_username
        appDetails = InsuranceClaimDetails.objects.filter(claim_status = 'Pending')
        return render(request,'insuranceHome.html',{
            'user': insuranceStaffName,
            'appDetails': appDetails,
        })

def logout_user(request):
    print("yes")
    # name = signing.loads(user)
    logout(request)
    print("Loggedout")
    username = EmployeeDetails.objects.get(employee_username=insuranceStaffName)
    test = HospitalPortal.objects.get(username = username.employee_username)
    test.session='N'
    test.save()
    # now = datetime.now()
    # dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    #logger.info("USERNAME:  " username.patient_name "   LOGOUTIME:   "+dt_string)
    return redirect('/Login')

class newPolicies(View):
    def get(self,request):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        appDetails = InsurancePolicies.objects.all()
        return render(request,'newPolicies.html',{
            'user':insuranceStaffName,
            'newInsurancePolicyForm': newInsurancePolicyForm,
            'appDetails': appDetails,
        })
    def post(self,request):
        msgS = ''
        try:
            form = newInsurancePolicyForm(request.POST)
            if form.is_valid():
                policy_name = form.cleaned_data.get('policy_name')
                coverage_plans = form.cleaned_data.get('coverage_plans')
                insurance_amt = form.cleaned_data.get('insurance_amt')
                print("going to save")
                InsurancePoliciesObj = InsurancePolicies(policy_name=policy_name,
                                            coverage_plans=coverage_plans,insurance_amt=insurance_amt)
                InsurancePoliciesObj.save()
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
            return redirect('/insurance/newPolicies')

class viewPolicies(View):
     def get(self, request):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        appDetails = InsurancePolicies.objects.all()
        return render(request,'viewPolicies.html',{
            'user':insuranceStaffName,
            'newInsurancePolicyForm':newInsurancePolicyForm,
            'appDetails': appDetails,
        })
        
class checkClaims(View):
    def get(self, request, id):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        claimDetails = InsuranceClaimDetails.objects.get(claim_id=id)   
        print(claimDetails.claim_id)
        print(claimDetails.patient_id)
        registerDetails = InsuranceClaimRegister.objects.all()
        policyDetails = InsurancePolicies.objects.all()
        policy_number =0
        amt =0
        current_claimed_amt = claimDetails.claim_amt
        remaining_claim_amt = 0
        print("hello")
        for a in policyDetails:
            if a.policy_name == claimDetails.policy_name:
                policy_number = a .policy_id
                amt = a.insurance_amt  #total policy amt
                print("hi")
                print(policy_number)
        print(policy_number)
        checkClaimTotal = InsuranceClaimDetails.objects.filter(patient_id = claimDetails.patient_id)
        for i in checkClaimTotal:
            if (i.claim_transaction_status == 'Approved' and 
               i.patient_firstname.casefold() == claimDetails.patient_firstname.casefold() and
               i.patient_lastname.casefold() == claimDetails.patient_lastname.casefold() and
               i.policy_name == claimDetails.policy_name):
                current_claimed_amt+= i.claim_amt
                print(current_claimed_amt)



        found =0
        for a in registerDetails:
            if(a.patient_id == claimDetails.patient_id and 
                a.patient_firstname.casefold() == claimDetails.patient_firstname.casefold() and
                a.patient_lastname.casefold() == claimDetails.patient_lastname.casefold() and
                a.policy_id == policy_number and amt >= current_claimed_amt):
                print("Approved")
                print(claimDetails.patient_firstname)
                claimDetails.claim_status = 'Approved'
                claimDetails.claim_transaction_status = 'Approved'
                claimDetails.claim_transaction_id = '#C{}'.format(uuid.uuid1().time_low)
                claimDetails.save()
                remaining_claim_amt = amt - current_claimed_amt
                found = 1
                print("Saved")

        if(found):
           # messages.success(request, 'Approved on Verification')
            messages.success(request, 'Approved on Verification with remaining claim amt ${}'.format(remaining_claim_amt))
            #msgS = "Approved on Verification"
            print("true")
        else:
            claimDetails.claim_status = 'Rejected'
            claimDetails.save()
            #msgE = "Rejected on Verification"
            messages.error(request, 'Rejected on Verification')
            print("false")
        
        print("in finally block")
        '''
        messages.add_message(request, messages.SUCCESS if msgS else messages.ERROR,
                                (msgS if not msgS == '' else msgE),
                                extra_tags='callout callout-success calloutCustom lead' if msgS else 'callout callout-danger calloutCustom lead')
        '''
        appDetails = InsuranceClaimDetails.objects.filter(claim_status = 'Pending')

        return render(request,'insuranceHome.html',{
            'user':insuranceStaffName,
             'appDetails': appDetails,
        })

class viewClaimRequests(View):
    def get(self,request):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        appDetails = InsuranceClaimDetails.objects.all()
        return render(request,'viewClaimRequests.html',{
            'user':insuranceStaffName,
            'appDetails': appDetails,
        })

class insurancePayments(View):
    def get(self,request):
        if not (request.user.is_authenticated):
            return redirect('/Login')
        appDetails = InsuranceClaimDetails.objects.filter(claim_transaction_status = 'Done')
        return render(request,'insurancePayments.html',{
            'user':insuranceStaffName,
            'appDetails': appDetails,
        })






            
