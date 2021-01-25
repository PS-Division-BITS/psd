from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView
from rest_framework.decorators import api_view

from apps.accounts.models import User
from server.constants import UserType, CampusType, ApplicationsStatus, TransferType, ThesisLocaleType
from apps.tms.models import ActiveUserProfile, PS2TSTransfer, TS2PSTransfer
from apps.tms.tools.export import getFileHod
from apps.tms.utils.shared_utils import update_application, clean_list

# without authentication
class HodData(APIView):
    def get(self, request, *args, **kwargs):
        try:
            active_user = ActiveUserProfile.objects.get(email=request.user.email)
        except Exception:
            return Response(
                data = {
                    'error': True,
                    'message': 'Access Denied. User not present in active user list',
                    'data': {},
                },
                status = status.HTTP_404_NOT_FOUND
            )
        if not request.user.is_superuser and active_user.user_type != UserType.HOD.value:
            return Response(
                data = {
                    'error': True,
                    'message': 'Access Denied. HOD login required',
                    'data': {},
                },
                status = status.HTTP_403_FORBIDDEN
            )
        try:
            current_user = request.user
            current_user_alias = 'Head Of Department'
            campus_alias = CampusType._member_names_[active_user.campus]
            application_type = int(request.query_params.get('application_type'))

            if application_type == TransferType.TS2PS.value:
                # TS2PS Application

                # applications where approval is pending
                pending_applications_qs = TS2PSTransfer.objects.filter(
                    hod_email = current_user.email,
                    is_hod_approved = ApplicationsStatus.PENDING.value,
                ).values(
                    'applicant__email',
                    'cgpa', 'reason_for_transfer', 'name_of_org',
                    'is_hod_approved',
                )
                pending_applications_list = list(pending_applications_qs)
                pending_applications_list = clean_list(pending_applications_list)
                for application in pending_applications_list:
                    try:
                        user_obj = User.objects.get(email=application['applicant__email'])
                        application.update({'applicant_username': user_obj.username})
                        application.update({'applicant_first_name': user_obj.first_name})
                        application.update({'applicant_last_name': user_obj.last_name})
                    except Exception as e:
                        pass

                # approved applications
                approved_applications_qs = TS2PSTransfer.objects.filter(
                    hod_email = current_user.email,
                    is_hod_approved__gt = ApplicationsStatus.PENDING.value,
                ).values(
                    'applicant__email',
                    'cgpa', 'name_of_org', 'reason_for_transfer',
                    'is_hod_approved',
                )
                approved_applications_list = list(approved_applications_qs)
                approved_applications_list = clean_list(approved_applications_list)
                for application in approved_applications_list:
                    try:
                        user_obj = User.objects.get(email=application['applicant__email'])
                        application.update({'applicant_username': user_obj.username})
                        application.update({'applicant_first_name': user_obj.first_name})
                        application.update({'applicant_last_name': user_obj.last_name})
                    except Exception as e:
                        pass

                attributes_for_display = [
                    {'display': 'Student ID', 'prop':'applicant__user__username'},
                    {'display':'Student First Name','prop':'applicant__user__first_name'},
                    {'display':'Student Last Name','prop':'applicant__user__last_name'},
                    {'display':'CGPA','prop':'cgpa'},
                    {'display':'Transfer reason','prop':'reason_for_transfer'},
                    {'display':'Organisation','prop':'name_of_org'},
                    {'display':'Status', 'prop':'status'}
                ]
                return Response(
                    data = {
                        'error': False,
                        'message': 'Success',
                        'data': {
                            'user':{
                                'username': current_user.username,
                                'designation': current_user_alias,
                                'campus': campus_alias,
                                'email': current_user.email
                            },
                            'student_pending_attributes': attributes_for_display[:-1],
                            'student_approved_attributes': attributes_for_display,
                            'data_pending': [a for a in pending_applications_list],
                            'data_approved': [a for a in approved_applications_list],
                        },
                    },
                    status = status.HTTP_200_OK
                )

            elif application_type == TransferType.PS2TS.value:
                # PS2TS Application

                # applications where approval is pending
                pending_applications_qs = PS2TSTransfer.objects.filter(
                    hod_email = current_user.email,
                    is_supervisor_approved__gt = ApplicationsStatus.PENDING.value,
                    is_hod_approved = ApplicationsStatus.PENDING.value,
                ).values(
                    'applicant__email',
                    'cgpa', 'thesis_locale', 'supervisor_email',
                    'thesis_subject', 'name_of_org', 'expected_deliverables',
                    'is_hod_approved', 'comments_from_supervisor',
                )
                # updating with supervisor details
                supervisor_emails = pending_applications_qs.values('supervisor_email')
                supervisor_details = []
                for supervisor_email in list(supervisor_emails):
                    try:
                        obj = ActiveUserProfile.objects.get(
                            email=supervisor_email['supervisor_email'],
                            user_type=UserType.SUPERVISOR.value,
                        )
                    except Exception as e:
                        return Response(
                            data = {
                                'error': True,
                                'message': 'Access Denied. Supervisor {0} not present in active user list'.format(supervisor_email['supervisor_email']),
                                'data': {},
                            },
                            status = status.HTTP_404_NOT_FOUND
                        )
                    supervisor_details.append({'supervisor_name': '{0} {1}'.format(obj.first_name, obj.last_name)})
                pending_applications_list = list(pending_applications_qs)
                for x, y in zip(pending_applications_list, supervisor_details):
                    x.update(y)
                pending_applications_list = clean_list(pending_applications_list)
                for application in pending_applications_list:
                    try:
                        user_obj = User.objects.get(email=application['applicant__email'])
                        application.update({'applicant_username': user_obj.username})
                        application.update({'applicant_first_name': user_obj.first_name})
                        application.update({'applicant_last_name': user_obj.last_name})
                    except Exception as e:
                        pass

                # approved applications
                approved_applications_qs = PS2TSTransfer.objects.filter(
                    hod_email = current_user.email,
                    is_supervisor_approved__gt = ApplicationsStatus.PENDING.value,
                    is_hod_approved__gt = ApplicationsStatus.PENDING.value,
                ).values(
                    'applicant__email',
                    'cgpa', 'thesis_locale', 'supervisor_email',
                    'thesis_subject', 'name_of_org', 'expected_deliverables',
                    'is_hod_approved', 'comments_from_supervisor',
                )
                # updating with supervisor email
                supervisor_emails = approved_applications_qs.values('supervisor_email')
                supervisor_details = []
                for supervisor_email in supervisor_emails:
                    try:
                        obj = ActiveUserProfile.objects.get(
                            email=supervisor_email['supervisor_email'],
                            user_type=UserType.SUPERVISOR.value,
                        )
                    except Exception as e:
                        return Response(
                            data = {
                                'error': True,
                                'message': 'Access Denied. Supervisor {0} not present in active user list'.format(supervisor_email['supervisor_email']),
                                'data': {},
                            },
                            status = status.HTTP_404_NOT_FOUND
                        )
                    supervisor_details.append({'supervisor_name': '{0} {1}'.format(obj.first_name, obj.last_name)})
                approved_applications_list = list(approved_applications_qs)
                for x, y in zip(pending_applications_list, supervisor_details):
                    x.update(y)
                approved_applications_list = clean_list(approved_applications_list)
                for application in approved_applications_list:
                    try:
                        user_obj = User.objects.get(email=application['applicant__email'])
                        application.update({'applicant_username': user_obj.username})
                        application.update({'applicant_first_name': user_obj.first_name})
                        application.update({'applicant_last_name': user_obj.last_name})
                    except Exception as e:
                        pass

                attributes_for_display = [
                    {'display': 'Student ID', 'prop':'applicant__user__username'},
                    {'display':'Student First Name','prop':'applicant__user__first_name'},
                    {'display':'Student Last Name','prop':'applicant__user__last_name'},
                    {'display':'CGPA','prop':'cgpa'},
                    {'display':'Supervisor Email', 'prop':'supervisor_email'},
                    {'display':'Thesis Location','prop':'thesis_locale_alias'},
                    {'display':'Thesis Subject','prop':'thesis_subject'},
                    {'display':'Organisation','prop':'name_of_org'},
                    {'display':'Expected Deliverables','prop':'expected_deliverables'},
                    {'display':'Supervisor comments','prop':'comments_from_supervisor'},
                    {'display':'Status', 'prop':'status'}
                ]
                return Response(
                    data = {
                        'error': False,
                        'message': 'Success',
                        'data': {
                            'user':{
                                'username': current_user.username,
                                'designation': current_user_alias,
                                'campus': campus_alias,
                                'email': current_user.email
                            },
                            'student_pending_attributes': attributes_for_display[:-1],
                            'student_approved_attributes': attributes_for_display,
                            'data_pending': [a for a in pending_applications_list],
                            'data_approved': [a for a in approved_applications_list],
                        },
                    },
                    status = status.HTTP_200_OK
                )
            else:
                raise Exception('Application type not configured.')
        except Exception as e:
            return Response(
                data = {
                    'error': True,
                    'message': 'Error. '+str(e),
                    'data': {
                        'username': current_user.username,
                        'designation': current_user_alias,
                        'campus': campus_alias,
                        'email': current_user.email
                    },
                },
                status = status.HTTP_404_NOT_FOUND
            )

# without authentication
class ApproveTransferRequest(APIView):
    def post(self, request, *args, **kwargs):
        try:
            active_user = ActiveUserProfile.objects.get(email=request.user.email)
        except Exception as e:
            return Response(
                data = {
                    'error': True,
                    'message': 'Access Denied. User not present in active user list.',
                    'data': {},
                },
                status = status.HTTP_404_NOT_FOUND
            )
        if not request.user.is_superuser and active_user.user_type != UserType.HOD.value:
            return Response(
                data = {
                    'error': True,
                    'message': 'Access Denied. HOD login required',
                    'data': {},
                },
                status = status.HTTP_403_FORBIDDEN
            )
        applicant = request.data.get('student_username')
        application_type = int(request.data.get('application_type'))
        approved_by = active_user.user_type
        comments = request.data.get('comments')
        status_data = request.data.get('status')
        saved = update_application(applicant, application_type, approved_by, status_data, comments)
        if saved:
            return Response(
                data = {
                    'error': False,
                    'message': 'Application approved',
                    'data': {},
                },
                status = status.HTTP_200_OK
            )
        else:
            return Response(
                data = {
                    'error': True,
                    'message': 'Application update failed',
                    'data': {},
                },
                status = status.HTTP_500_INTERNAL_SERVER_ERROR
            )

# without authentication
class ExportHod(APIView):
    def get(self, request, *args, **kwargs):
        try:
            active_user = ActiveUserProfile.objects.get(email=request.user.email)
        except Exception:
            return Response(
                data = {
                    'error': True,
                    'message': 'Access Denied. User not present in active user list',
                    'data': {},
                },
                status = status.HTTP_404_NOT_FOUND
            )
        if not request.user.is_superuser and active_user.user_type != UserType.HOD.value:
            return Response(
                data = {
                    'error': True,
                    'message': 'Access Denied. HOD login required',
                    'data': {},
                },
                status = status.HTTP_403_FORBIDDEN
            )
        response = getFileHod(request, int(request.query_params.get('type')))
        return response

# Only here for testing, mote to shared_utils.py later
def clean_list(application_list):
    for data in application_list:
        try:
            if 'thesis_locale' in data:
                data['thesis_locale_alias'] = ThesisLocaleType._member_names_[data.pop('thesis_locale')]
            if 'is_supervisor_approved' in data:
                status_alias = ApplicationsStatus._member_names_[data.pop('is_supervisor_approved')]
                data['status'] = status_alias
            elif 'is_hod_approved' in data:
                status_alias = ApplicationsStatus._member_names_[data.pop('is_hod_approved')]
                data['status'] = status_alias
        except Exception as e:
            print('error in shared_utils.clean_list')
            print(e) # left for debugging
    return application_list