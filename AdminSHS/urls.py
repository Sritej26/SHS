from . import views
from django.urls import URLPattern, path, re_path
app_name = 'Admin'

urlpatterns = [
    path('', views.adminHome.as_view(), name='adminHome'),
    path('adminHome', views.adminHome.as_view(), name='adminHome'),
    re_path('createEmployeeRecords', views.createEmployeeRecords.as_view(), name='createEmployeeRecords'),
    re_path('viewEmployeeRecords', views.viewEmployeeRecords.as_view(), name='viewEmployeeRecords'),
    re_path('editEmployeeRecords', views.editEmployeeRecords.as_view(), name='editEmployeeRecords'),
    path('showLogFiles', views.showLogFiles.as_view(), name='showLogFiles'),
    re_path(r'^updateEmployeeDetails/(?P<id>\d+)/$', views.updateEmployeeDetails.as_view(), name='updateEmployeeDetails'),
    re_path(r'^updateEmployeeDetails/delete/(?P<id>\d+)/$', views.deleteEmployeeRecord.as_view(), name='deleteEmployeeRecord'),
    re_path('appointmentTransactionRequests', views.appointmentTransactionRequests.as_view(), name='appointmentTransactionRequests'),
    re_path('insuranceTransactionRequests', views.insuranceTransactionRequests.as_view(), name='insuranceTransactionRequests'),
    re_path('showInternalFiles', views.showInternalFiles.as_view(), name='showInternalFiles'),
    re_path('showHospitalFiles', views.showHospitalFiles.as_view(), name='showHospitalFiles'),
    re_path('showInsuranceFiles', views.showInsuranceFiles.as_view(), name='showInsuranceFiles'),
    re_path('showLabFiles', views.showLabFiles.as_view(), name='showLabFiles'),
    re_path('showDoctorFiles', views.showDoctorFiles.as_view(), name='showDoctorFiles'),

]