from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('index2', views.index2, name='index2'),
     path('index3', views.index3, name='index3'),
      path('starter', views.index3, name='index3'),
       path('iframe', views.index3, name='index3')

]