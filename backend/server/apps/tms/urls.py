from django.urls import path

from apps.tms.views import (student_views, hod_views)

urlpatterns = [
    path('student/PS2TS/', student_views.PS2TS.as_view()),
    path('student/TS2PS/', student_views.TS2PS.as_view()),

    # HOD urls
    path('hod/data/', hod_views.HodData.as_view()),
    path('hod/approve-transfer-request/', hod_views.ApproveTransferRequest.as_view()),

]

# data related urls
urlpatterns += [
    # hod urls
    path('data/export-hod/', hod_views.ExportHod.as_view()),
]