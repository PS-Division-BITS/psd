from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView

from apps.tms.serializers import PS2TSTransferSerializer,TS2PSTransferSerializer
from apps.tms.models import PS2TSTransfer, TS2PSTransfer, ActiveUserProfile
from apps.tms.utils.ad_utils import fetch_ps2ts_list, fetch_ts2ps_list
from server.constants import TransferType,ApplicationsStatus

class ADdashboard(APIView):
    def get(self, request, *args, **kwargs):
        try:
            application_type = int(request.data['type'])  
            if application_type == TransferType.PS2TS.value:
                data = fetch_ps2ts_list()
            elif int(application_type) == TransferType.TS2PS.value:
                data = fetch_ts2ps_list()
            else:
                data = []
                return Response(
                    data={
                        'success' : False,
                        'message' : 'incorrect value for application type',
                        'data' : data
                    },
                    status = status.HTTP_400_BAD_REQUEST
                )    
            return Response(
                data={
                    'success' : True,
                    'message' : 'list has been fetched',
                    'data' : data,
                },
                status = status.HTTP_200_OK
            )                
        except:
            return Response(
                data = {
                    'message' : 'no data-type requested',
                },
                status = status.HTTP_200_OK
            )

    def post(self, request):
        active_user = ActiveUserProfile.objects.get(email=request.user.email)
        # active_user = ActiveUserProfile.objects.get(email='ad@ad.com')
        active_student = ActiveUserProfile.objects.get(email=request.data['applicant_email'])

        application_type = int(request.data['type'])
        comments = request.data['comments']

        if application_type == TransferType.PS2TS.value:
            form = PS2TSTransfer.objects.get(applicant=active_student)
        elif application_type == TransferType.TS2PS.value:
            form = TS2PSTransfer.objects.get(applicant=active_student)
        else:
            return Response(
                data={
                    'success' : False,
                    'message' : 'incorrect value of application_type',
                },
                status = status.HTTP_400_BAD_REQUEST
            )

        form.is_ad_approved = ApplicationsStatus.REJECTED.value
        form.comments_from_ad = comments
        form.save()
        return Response(
            data = {
                'success' : True,
                'message' : 'Application has been rejected'
            },
            status = status.HTTP_200_OK
        )
        




