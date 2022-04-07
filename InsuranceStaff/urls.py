# @author - aishwarya
from django.urls import path, re_path
from . import views
app_name = 'InsuranceStaff'

urlpatterns = [
    re_path(r'^insuranceHome/(?P<id>(.*))$', views.insuranceHome.as_view(), name='insuranceHome'),
    path('newPolicies/', views.newPolicies.as_view(), name='newPolicies'),
    path('viewPolicies/', views.viewPolicies.as_view(), name='viewPolicies'),
    re_path(r'^checkClaims/(?P<id>\d+)/$', views.checkClaims.as_view(), name='checkClaims'),
    path('viewClaimRequests/', views.viewClaimRequests.as_view(), name='viewClaimRequests'),
    path('insurancePayments/', views.insurancePayments.as_view(), name='insurancePayments'),    
    path('logout', views.logout_user)
   ]