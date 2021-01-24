from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView

from apps.tms.models import ActiveUserProfile, PS2TSTransfer, TS2PSTransfer
from apps.tms.serializers import PS2TSTransferSerializer, TS2PSTransferSerializer


#without authentication
class PS2TS(APIView):
    def post(self, request, *args, **kwargs):
        try:
            #hardcoded user for now
            # active_user = ActiveUserProfile.objects.get(email='nrupeshsurya@gmail.com')
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
            serializer = PS2TSTransferSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(applicant=active_user,cgpa=float(active_user.cgpa))
                return Response(
                    data={
                        'success' : True,
                        'message' : 'PS2TS form successfully saved',
                        'data' : {}
                    },
                    status = status.HTTP_201_CREATED
                )
            return Response(
                data={
                    'success' : False,
                    'message' : 'PS2TS form not saved',
                    'data' : serializer.errors,
                },
                status = status.HTTP_400_BAD_REQUEST
            )
        
class TS2PS(APIView):
    def post(self, request, *args, **kwargs):
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
            serializer = TS2PSTransferSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(applicant=active_user, cgpa=active_user.cgpa)
                return Response(
                    data = {
                        'success': True,
                        'message': 'TS2PS form saved successfully',
                        'data': {},
                    },
                    status = status.HTTP_201_CREATED
                )
            return Response(
                data={
                    'success' : False,
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
            try:
                ps2ts_form = PS2TSTransfer.objects.get(applicant=active_user)
                serializer = PS2TSTransferSerializer(ps2ts_form)
                return Response(
                    data = {
                        'success' : True,
                        'message' : 'PS2TS form exists',
                        'data' : serializer.data,
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
                    },
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data={
                    'success' : False,
                    'message' : 'Form does not exist',
                    'data' : {},
                    },
                    status=status.HTTP_204_NO_CONTENT
                )
                

