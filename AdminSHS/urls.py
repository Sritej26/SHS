from . import views
from django.urls import URLPattern, path, re_path
app_name = 'AdminSHS'

urlpatterns = [
    # path('', views.adminHome.as_view(), name='adminHome'),
    re_path(r'^adminHome/(?P<id>(.*))$', views.adminHome.as_view(), name='adminHome'),
    re_path(r'^adminHome/(?P<user>(.*))$', views.adminHome.as_view(), name='adminHome'),
    re_path(r'^createEmployeeRecords/(?P<id>(.*))$', views.createEmployeeRecords.as_view(), name='createEmployeeRecords'),
    # re_path('createEmployeeRecords', views.createEmployeeRecords.as_view(), name='createEmployeeRecords'),
    re_path(r'^viewEmployeeRecords/(?P<id>(.*))$', views.viewEmployeeRecords.as_view(), name='viewEmployeeRecords'),
    re_path(r'^editEmployeeRecords/(?P<id>(.*))$', views.editEmployeeRecords.as_view(), name='editEmployeeRecords'),
    re_path(r'^showLogFiles/(?P<id>(.*))$', views.showLogFiles.as_view(), name='showLogFiles'),
    re_path('showLogFiles', views.showLogFiles.as_view(), name='showLogFiles'),
    re_path(r'^updateEmployeeDetails/update/(?P<id>(.*))/(?P<a_id>(.*))$', views.updateEmployeeDetails.as_view(), name='updateEmployeeDetails'),
    re_path(r'^updateEmployeeDetails/delete/(?P<id>(.*))/(?P<a_id>(.*))$', views.deleteEmployeeRecord.as_view(), name='deleteEmployeeRecord'),
    re_path(r'^appointmentTransactionRequests/(?P<id>(.*))/(?P<a_id>(.*))$', views.appointmentTransactionRequests.as_view(), name='appointmentTransactionRequests'),
    re_path(r'^insuranceTransactionRequests/(?P<id>(.*))(?P<a_id>(.*))$', views.insuranceTransactionRequests.as_view(), name='insuranceTransactionRequests'),
    re_path(r'^showInternalFiles/(?P<id>(.*))$', views.showInternalFiles.as_view(), name='showInternalFiles'),
    re_path(r'^showHospitalFiles/(?P<id>(.*))$', views.showHospitalFiles.as_view(), name='showHospitalFiles'),
    re_path(r'^showInsuranceFiles/(?P<id>(.*))$', views.showInsuranceFiles.as_view(), name='showInsuranceFiles'),
    re_path(r'^showLabFiles/(?P<id>(.*))$', views.showLabFiles.as_view(), name='showLabFiles'),
    re_path(r'^showDoctorFiles/(?P<id>(.*))$', views.showDoctorFiles.as_view(), name='showDoctorFiles'),
]