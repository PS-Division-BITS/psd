from django.conf import settings

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import traceback

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_auth.registration.views import SocialLoginView
from rest_framework.authtoken.models import Token


class GoogleLogin(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client

class VerifyToken(APIView):
    def post(self ,request):
        try:
            user = Token.objects.get(key=request.data['key']).user
            return Response(
                data={
                    'success': True, 'message': 'Success: User found',
                    'data':{
                        'email': user.email,
                        'username': user.username,
                        'first_name': user.first_name,
                        'last_name': user.last_name
                    }
                }, status=status.HTTP_200_OK
            )
        except Exception as e:
            if settings.DEBUG:
                traceback.print_exc()
                print(request.data)
            return Response(
                data={
                    'success': False, 'message': str(e)
                }, status=status.HTTP_404_NOT_FOUND
            )
