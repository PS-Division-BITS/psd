from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView

from apps.tms.models import ActiveUserProfile, PS2TSTransfer, TS2PSTransfer
from apps.tms.serializers import PS2TSTransferSerializer, TS2PSTransferSerializer
from server.constants import TransferType
from apps.tms.utils.student_utils import *
from apps.tms.utils.shared_utils import get_deadline_status


#without authentication
class PS2TS(APIView):
    def get(self, request):
        try:
            active_user = ActiveUserProfile.objects.get(email=request.user.email)
            if not active_user.is_active_tms:
                raise Exception('Access Denied. User not present in active user list')
        except Exception:
            return Response(
                data = {
                    'success': False,
                    'message': 'Access Denied. User not present in active user list',
                    'data': {},
                },
                status = status.HTTP_403_FORBIDDEN
            )
        else:
            data = {
            'hod_email_list' : hod_data(active_user),
            'student_name' : str(active_user.first_name+" "+active_user.last_name),
            'student_id' : active_user.username,
            'student_branch' : get_branch_from_branch_code(active_user.username[4:6])+get_branch_from_branch_code(active_user.username[6:8]),
            'contact' : active_user.contact,
            }
            return Response(
                data = {
                    'success' : True,
                    'message' : 'PS2TS form fetched',
                    'data': data
                }
            )
        
    def post(self, request, *args, **kwargs):
        try:
            active_user = ActiveUserProfile.objects.get(email=request.user.email)
            if (not active_user.is_active_tms) and (get_deadline_status(TransferType.PS2TS.value)) :
                raise Exception('Access Denied. User not present in active user list')
        except Exception:
            return Response(
                data = {
                    'success': False,
                    'message': 'Access Denied. User not present in active user list',
                    'data': {},
                },
                status = status.HTTP_403_FORBIDDEN
            )
        else:
            serializer = PS2TSTransferSerializer(data=request.data)
            invalid_supervisor = check_supervisor(request.data['supervisor_email'])
            invalid_contact = validate_contact(request.data['contact'])
            if serializer.is_valid(raise_exception=True):  
                if(not invalid_supervisor) and (not invalid_contact):
                    serializer.save(applicant=active_user,cgpa=float(active_user.cgpa))
                    return Response(
                        data={
                            'success' : True,
                            'invalid_contact' : invalid_contact,
                            'invalid_supervisor' : invalid_supervisor,
                            'message' : 'PS2TS form successfully saved',
                            'data' : {}
                        },
                        status = status.HTTP_201_CREATED
                    )
            return Response(
                data={
                    'success' : False,
                    'invalid_contact' : invalid_contact,
                    'invalid_supervisor' : invalid_supervisor,
                    'message' : 'supervisor mail/contact may be invalid',
                    'data' : serializer.errors,
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        
class TS2PS(APIView):
    def get(self, request):
        try:
            active_user = ActiveUserProfile.objects.get(email=request.user.email)
            if not active_user.is_active_tms:
                raise Exception('Access Denied. User not present in active user list')
        except Exception:
            return Response(
                data = {
                    'success': False,
                    'message': 'Access Denied. User not present in active user list',
                    'data': {},
                },
                status = status.HTTP_403_FORBIDDEN
            )
        else:
            data = {
            'hod_email_list' : hod_data(active_user),
            'student_name' : str(active_user.first_name+" "+active_user.last_name),
            'student_id' : active_user.username,
            'student_branch' : get_branch_from_branch_code(active_user.username[4:6])+get_branch_from_branch_code(active_user.username[6:8]),
            'contact' : active_user.contact,
            }
            return Response(
                data = {
                    'success' : True,
                    'message' : 'TS2PS form fetched',
                    'data': data
                }
            )
    
    def post(self, request, *args, **kwargs):
        try:
            active_user = ActiveUserProfile.objects.get(email=request.user.email)
            if (not active_user.is_active_tms) and (get_deadline_status(TransferType.TS2PS.value)) :
                raise Exception('Access Denied. User not present in active user list')
        except Exception:
            return Response(
                data = {
                    'success': False,
                    'message': 'Access Denied. User not present in active user list',
                    'data': {},
                },
                status = status.HTTP_403_FORBIDDEN
            )
        else:
            invalid_supervisor = check_supervisor(request.data['supervisor_email'])
            invalid_contact = validate_contact(request.data['contact'])
            serializer = TS2PSTransferSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                if(not invalid_supervisor) and (not invalid_contact):
                    serializer.save(applicant=active_user, cgpa=active_user.cgpa)
                    return Response(
                        data = {
                            'success': True,
                            'message': 'TS2PS form saved successfully',
                            'invalid_contact' : invalid_contact,
                            'invalid_supervisor' : invalid_supervisor,
                            'data': {},
                        },
                        status = status.HTTP_201_CREATED
                    )
            return Response(
                data={
                    'success' : False,
                    'invalid_contact' : invalid_contact,
                    'invalid_supervisor' : invalid_supervisor,
                    'message' : 'TS2PS form not saved',
                    'data' : serializer.errors,
                },
                status = status.HTTP_400_BAD_REQUEST
            )

class Dashboard(APIView):
    def get(self, request):
        try:
            active_user = ActiveUserProfile.objects.get(email=request.user.email)
            if not active_user.is_active_tms:
                raise Exception('Access Denied. User not present in active user list')
        except Exception:
            return Response(
                data = {
                    'success': False,
                    'message': 'Access Denied. User not present in active user list',
                    'data': {},
                },
                status = status.HTTP_403_FORBIDDEN
            )
        else:
            deadline_status_ps2ts = get_deadline_status(TransferType.PS2TS.value)
            deadline_status_ts2ps = get_deadline_status(TransferType.TS2PS.value)
            deadline_data = [deadline_status_ps2ts,deadline_status_ts2ps]
            try:
                ps2ts_form = PS2TSTransfer.objects.get(applicant=active_user)
                serializer = PS2TSTransferSerializer(ps2ts_form)
                return Response(
                    data = {
                        'success' : True,
                        'message' : 'PS2TS form exists',
                        'data' : serializer.data,
                        'deadline_data' : deadline_data
                    },
                    status= status.HTTP_200_OK
                )
            except:
                ts2ps_form = TS2PSTransfer.objects.get(applicant=active_user)
                serializer = TS2PSTransferSerializer(ts2ps_form)
                return Response(
                    data = {
                        'success' : True,
                        'message' : 'TS2PS form exists',
                        'data' : serializer.data,
                        'deadline_data' : deadline_data
                    },
                    status=status.HTTP_200_OK
                )
            finally:
                return Response(
                    data={
                    'success' : True,
                    'message' : 'Form does not exist',
                    'data' : {},
                    'deadline_data' : deadline_data
                    },
                    status=status.HTTP_204_NO_CONTENT
                )
                
