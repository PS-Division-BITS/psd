from django.urls import path

from apps.tms.views import (student_views, hod_views, supervisor_views, ad_views)

urlpatterns = [
    # student related URLs
    path('student/PS2TS/', student_views.PS2TS.as_view()),
    path('student/TS2PS/', student_views.TS2PS.as_view()),
    path('student/dashboard/',student_views.Dashboard.as_view()),

    # HOD urls
    path('hod/data/', hod_views.HodData.as_view()),
    path('hod/approve-transfer-request/', hod_views.ApproveTransferRequest.as_view()),

    # AD related URLs
    path('AD/dashboard/',ad_views.ADdashboard.as_view()),
    
    # supervisor related URLs
    path('supervisor/dashboard/', supervisor_views.supervisorView.as_view()),
    path('supervisor/approve_transfer_request/', supervisor_views.approve_transfer_request)
]

# data related urls
urlpatterns += [
    # hod urls
    path('data/export-hod/', hod_views.ExportHod.as_view()),
]