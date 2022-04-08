from django.urls import path, re_path
from . import views
app_name = 'HospitalStaff'
print("in URL")
urlpatterns = [
    re_path(r'^hospitalStaffHome/(?P<id>(.*))$', views.hospitalStaffHome.as_view(), name='hospitalStaffHome'),
    #path('activate-user/<uidb64>/<token>',views.activate_user1, name='activate'),
    #path('', views.staffHome.as_view(), name='staffHome'),
    path('createRecord',views.createRecord.as_view(),name='createRecord'),
    # path('viewDetails',views.viewDetails.as_view(),name='viewDetails'),
    path('viewDetails1',views.viewDetails1.as_view(),name='viewDetails1'),
    re_path('search',views.search,name='search'),
    re_path(r'^checkAppointmets/(?P<id>\d)/$',views.checkAppointmets.as_view(),name='checkAppointmets'),
    re_path(r'^edit/(?P<id>\d)/$',views.edit.as_view(),name='edit'),
    path('approveAppointment',views.approveAppointment.as_view(),name='approveAppointment'),
    path('transactions',views.transactions.as_view(),name='transactions'),
    path('updatepersonalinfo',views.updatepersonalinfo.as_view(),name='updatepersonalinfo'),
    path('logout', views.logout_user)

    #re_path(r'^approveAppointment/',views.approveAppointment.as_view(),name='approveAppointment'),
    # re_path('searchDiagnosis/',views.searchDiagnosis,name='searchDiagnosis'),
    # re_path('searchPrescription/',views.searchPrescription,name='searchPrescription'),
    
    #re_path(r'^approveAppointment/updateStatus/(?P<id>\d)/$', views.approveAppointment.as_view(), name='approveAppointment'),
    #url(r'^approveAppointment$',views.approveAppointment,name='approveAppointment' )
    
]