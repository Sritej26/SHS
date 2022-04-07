from django.urls import URLPattern, path,re_path
from . import views
app_name="LabStaff"

urlpatterns = [
    re_path(r'^labStaffHome/(?P<user>(.*))$', views.labStaffHome.as_view(), name='labStaffHome'),
    re_path(r'^viewRequests/(?P<user>(.*))$', views.viewRequests.as_view(), name='viewRequests'),
    re_path(r'^addLabRecord/(?P<user>(.*))$', views.addLabRecord.as_view(), name='addLabRecord'),
    re_path(r'^updateLabRecord/(?P<user>(.*))$', views.updateLabRecord.as_view(), name='updateLabRecord'),
    re_path(r'^viewLabRecord/(?P<user>(.*))$', views.viewLabRecord.as_view(), name='viewLabRecord'),
     re_path(r'^logout/(?P<user>(.*))$', views.logout_user)

    # path('labStaffHome', views.labStaffHome.as_view(), name='labStaffHome'),
    # path('viewRequests', views.viewRequests.as_view(), name='viewRequests'),
    # path('addLabRecord', views.addLabRecord.as_view(), name='addLabRecord'),
    # path('updateLabRecord', views.updateLabRecord.as_view(), name='updateLabRecord'),
    # path('viewLabRecord', views.viewLabRecord.as_view(), name='viewLabRecord')
]