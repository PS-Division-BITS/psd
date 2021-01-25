from apps.tms.models import ActiveUserProfile, PS2TSTransfer, TS2PSTransfer
from apps.tms.serializers import PS2TSTransferSerializer, TS2PSTransferSerializer
from server.constants import UserType, CampusType, ApplicationsStatus
from apps.tms.utils.shared_utils import update_application, clean_list, resp

import json
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
class supervisorView(APIView):

    def get(self, request):
        response = Response()
        current_user = request.user
        current_user_alias = 'Student Supervisor'
        try:
            #hardcoded user for now
            userProfile = ActiveUserProfile.objects.get(email="mudit@gmail.com")
            # active_user = ActiveUserProfile.objects.get(email=request.user.email)
            if not userProfile.is_active_tms or userProfile.user_type<1: #checks if at least supervisor
                raise Exception('Access Denied. User not present in active user list')
        except Exception:
            return resp(False, "Access Denied. User not present in active user list", {}, status.HTTP_403_FORBIDDEN)
        campus_alias = CampusType._member_names_[userProfile.campus]
        try:
            # applications where approval is pending
            pending_applications_qs = PS2TSTransfer.objects.filter(
                supervisor_email = current_user.email,
                is_supervisor_approved = ApplicationsStatus.PENDING.value,
            ).values(
                'applicant__username',
                'applicant__first_name', 'applicant__last_name',
                'cgpa', 'thesis_locale', 'supervisor_email',
                'thesis_subject', 'name_of_org', 'expected_deliverables'
            )

            pending_applications_list = list(pending_applications_qs)
            pending_applications_list = clean_list(pending_applications_list)
            # approved applications
            approved_applications_qs = PS2TSTransfer.objects.filter(
                supervisor_email = current_user.email,
                is_supervisor_approved__gt=ApplicationsStatus.PENDING.value,
            ).values(
                'applicant__username',
                'applicant__first_name', 'applicant__last_name',
                'cgpa', 'thesis_locale', 'supervisor_email',
                'thesis_subject', 'name_of_org', 'expected_deliverables',
                'is_supervisor_approved',
            )
            approved_applications_list = list(approved_applications_qs)
            approved_applications_list = clean_list(approved_applications_list)
            data = {}
            data['user'] = {
                'username': current_user.username,
                'designation': current_user_alias,
                'campus': campus_alias,
                'email': current_user.email

            }
            attributes_for_display = [
                {'display': 'Student ID', 'prop':'applicant__username'},
                {'display':'Student First Name','prop':'applicant__first_name'},
                {'display':'Student Last Name','prop':'applicant__last_name'},
                {'display':'CGPA','prop':'cgpa'},
                {'display': 'Supervisor (on-campus) email', 'prop':'supervisor_email'},
                {'display':'Thesis Location','prop':'thesis_locale_alias'},
                {'display':'Thesis Subject','prop':'thesis_subject'},
                {'display':'Organisation','prop':'name_of_org'},
                {'display':'Expected Deliverables','prop':'expected_deliverables'},
                {'display': 'Status', 'prop':'status'},
            ]
            data['student_pending_attributes'] = attributes_for_display[:-1]
            data['student_approved_attributes'] = attributes_for_display
            data['data_pending'] = [a for a in pending_applications_list]
            data['data_approved']= [a for a in approved_applications_list]
            response = resp(True, "Applications Present", data, status.HTTP_200_OK)

        except Exception as e:
            data = {
                'username': current_user.username,
                'designation': current_user_alias,
                'campus': campus_alias,
                'email': current_user.email

            }
            print(e)
            response = resp(False,"No Applications Present", data, status.HTTP_204_NO_CONTENT)
        return response



#not sure about this function
def approve_transfer_request(request):
    applicant = request.data['student_username']
    status = request.data['status']
    approved_by = UserType.SUPERVISOR.value
    application_type = int(request.data['application_type'])
    comments = request.data['comments']
    saved = update_application(applicant, application_type, approved_by, status, comments)
    if saved:
        return resp(True, "Application approved", {},status.HTTP_202_ACCEPTED)
    else:
        return resp(False, "Failed to Approve Application",{},status.HTTP_417_EXPECTATION_FAILED)
