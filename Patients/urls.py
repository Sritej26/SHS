# @author - aishwarya
from django.urls import path, re_path
from . import views
app_name = 'patient'

urlpatterns = [
    re_path(r'^nextAppointment/(?P<id>\d+)/$', views.nextAppointment.as_view(), name='nextAppointment'),
    re_path(r'^insuranceClaimRequest/(?P<id>(.*))/$', views.insuranceClaimRequest.as_view(), name='insuranceClaimRequest'),
    #re_path(r'^updateInsuranceClaimRequest/(?P<id>\d+)/$', views.updateInsuranceClaimRequest.as_view(), name='updateInsuranceClaimRequest'),
    #re_path(r'^registerPolicy/(?P<id>\d+)/$', views.registerPolicy.as_view(), name='registerPolicy'),
    re_path(r'^declineTransaction/(?P<id>\d+)/$', views.declineTransaction.as_view(), name='declineTransaction'),
    re_path(r'^approveTransaction/(?P<id>\d+)/$', views.approveTransaction.as_view(), name='approveTransaction'),
    re_path(r'^patientPayment/(?P<id>\d+)/$', views.patientPayment.as_view(), name='patientPayment'),
    
    re_path(r'^logout/(?P<id>(.*))$', views.logout_user),
    re_path(r'^home/(?P<id>(.*))$', views.patientHome.as_view(), name='patientHome'),
    re_path(r'^requestLabTests/(?P<id>(.*))$', views.requestLabTests.as_view(), name='requestLabTests'),
    re_path(r'^viewRecords/(?P<id>(.*))$', views.viewRecords.as_view(), name='viewRecords'),
    re_path(r'^updateAppointment/(?P<a_id>(.*))/(?P<id>(.*))$', views.updateAppointment.as_view(), name='updateAppointment'),
    re_path(r'^cancelAppointment/(?P<a_id>(.*))/(?P<id>(.*))$', views.cancelAppointment.as_view(), name='cancelAppointment'),
    re_path(r'^viewPrescription/(?P<a_id>(.*))/(?P<id>(.*))$', views.viewPrescription.as_view(), name='viewPrescription'),
    re_path(r'^profileUpdateRequest/(?P<id>(.*))$', views.profileUpdateRequest.as_view(), name='profileUpdateRequest'),
    re_path(r'^contactHelp/(?P<id>(.*))$', views.contactHelp.as_view(), name='contactHelp'),
    re_path(r'^bookAppointment/(?P<id>(.*))$', views.bookAppointment.as_view(), name='bookAppointment'),
    re_path(r'^registerPolicy/(?P<policy_id>(.*))/(?P<id>(.*))$', views.registerPolicy.as_view(), name='registerPolicy'),
    re_path(r'^updateInsuranceClaimRequest/(?P<claim_id>(.*))/(?P<id>(.*))$', views.updateInsuranceClaimRequest.as_view(), name='updateInsuranceClaimRequest'),



]