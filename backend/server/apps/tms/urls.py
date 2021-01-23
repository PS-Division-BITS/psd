from django.urls import path

from apps.tms.views import (student_views)

urlpatterns = [
    path('student/PS2TS/', student_views.PS2TS.as_view()),
    path('student/TS2PS/', student_views.TS2PS.as_view()),
    path('student/dashboard/',student_views.Dashboard.as_view()),
]
