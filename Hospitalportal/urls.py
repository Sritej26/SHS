from django.urls import path , include
from . import views
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('', views.Login.as_view(), name='Login'),
    path('accounts/login/', views.Login.as_view(), name='Login'),
    path('Register', views.Register, name='Register'),
    path('Registercheck', views.Registercheck.as_view(), name='Registercheck'),
    path('activate-user/<uidb64>/<token>',views.activate_user, name='activate'),
    path('password_reset/',auth_views.PasswordResetView.as_view(),name='password_reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(),name='password_reset_done'),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name='password_reset_confirm'),
    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(),name='password_reset_complete'),
]