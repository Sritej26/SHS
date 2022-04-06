"""SHS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path , include
from Patients import urls
from Doctors import urls

urlpatterns = [
    path('', include('Hospitalportal.urls')),
    path('adminSHS/', include('AdminSHS.urls', namespace='adminSHS')),
    path('admin/', admin.site.urls),
    path('patient/',include('Patients.urls')),
    path('labStaff/', include('LabStaff.urls')),
    path('doctors/', include('Doctors.urls', namespace='doctors')),
    path('insurance/', include('InsuranceStaff.urls', namespace='insuranceStaff')),
    path('hospitalStaff/',include('HospitalStaff.urls', namespace='hospitalStaff')),
]
