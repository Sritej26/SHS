from django.urls import URLPattern, path,re_path
from . import views
app_name="LabStaff"

urlpatterns = [
    re_path(r'^labStaffHome/(?P<id>(.*))$', views.labStaffHome.as_view(), name='labStaffHome'),
    re_path(r'^viewRequests/', views.viewRequests.as_view(), name='viewRequests'),
    re_path(r'^addLabRecord/', views.addLabRecord.as_view(), name='addLabRecord'),
    re_path(r'^updateLabRecord/', views.updateLabRecord.as_view(), name='updateLabRecord'),
    re_path(r'^viewLabRecord/', views.viewLabRecord.as_view(), name='viewLabRecord'),
    path('logout', views.logout_user)

    # path('labStaffHome', views.labStaffHome.as_view(), name='labStaffHome'),
    # path('viewRequests', views.viewRequests.as_view(), name='viewRequests'),
    # path('addLabRecord', views.addLabRecord.as_view(), name='addLabRecord'),
    # path('updateLabRecord', views.updateLabRecord.as_view(), name='updateLabRecord'),
    # path('viewLabRecord', views.viewLabRecord.as_view(), name='viewLabRecord')
]