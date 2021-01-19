from django.conf import settings
from django.contrib.auth import (
    authenticate, login, logout, get_user_model,
    user_logged_out
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import traceback

User = get_user_model()

class LoginView(APIView):
    def post(self, request):
        try:
            user = authenticate(
                request, username=request.data['username'],
                password=request.data['password']
            )
            if user is not None:
                login(request, user)
                return Response(
                    data={
                          'success':True, 'message':"Success: User logged in",
                          'data':{
                            'username': user.username,
                            'email': user.email,
                          }
                    }, status=status.HTTP_200_OK
                )
            else:
                return Response(
                    data={
                          'success':False, 'message':"User does not exists",
                          'data':{
                            'username': request.data['username'],
                          }
                    }, status=status.HTTP_200_OK
                )
        except Exception:
            if settings.DEBUG:
                traceback.print_exc()
            return Response(
                    data={
                          'success':False, 'message':"Internal Server Error",
                          'data':{
                            'username': request.data['username'],
                          }
                    }, status=status.HTTP_200_OK
                )


class LogoutView(APIView):
    def post(self ,request):
        user_logged_out.send(
            sender=request.user.__class__, request=request, user=request.user
            )
        logout(request)
        return Response(
                    data={
                          'success':True, 'message':"Success: User logged out",
                          'data':{
                            'username': request.data['username'],
                          }
                    }, status=status.HTTP_200_OK
                )
