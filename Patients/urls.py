# @author - aishwarya
from django.urls import path, re_path
from . import views
app_name = 'patient'

urlpatterns = [
    path('', views.patientHome.as_view(), name='patientHome'),
    re_path(r'^bookAppointment/(?P<id>\d+)/$', views.bookAppointment.as_view(), name='bookAppointment'),
    re_path(r'^updateAppointment/(?P<id>\d+)/$', views.updateAppointment.as_view(), name='updateAppointment'),
    re_path(r'^nextAppointment/(?P<id>\d+)/$', views.nextAppointment.as_view(), name='nextAppointment'),
    re_path(r'^insuranceClaimRequest/(?P<id>\d+)/$', views.insuranceClaimRequest.as_view(), name='insuranceClaimRequest'),
    re_path(r'^updateInsuranceClaimRequest/(?P<id>\d+)/$', views.updateInsuranceClaimRequest.as_view(), name='updateInsuranceClaimRequest'),
    re_path(r'^logout/(?P<id>\d+)/$', views.logout_user),
    re_path(r'^home/(?P<id>\d+)/$', views.patientHome.as_view(), name='patientHome'),
    re_path(r'^registerPolicy/(?P<id>\d+)/$', views.registerPolicy.as_view(), name='registerPolicy'),
    re_path(r'^declineTransaction/(?P<id>\d+)/$', views.declineTransaction.as_view(), name='declineTransaction'),
    re_path(r'^approveTransaction/(?P<id>\d+)/$', views.approveTransaction.as_view(), name='approveTransaction'),
    re_path(r'^patientPayment/(?P<id>\d+)/$', views.patientPayment.as_view(), name='patientPayment'),


]