from django.urls import include, path
from django.conf import  settings

from .views import LoginView, LogoutView


urlpatterns = [
    path('api/login/', LoginView.as_view()),
    path('api/logout/', LogoutView.as_view()),
]

# only for debugging while using browsable rest-api
if settings.DEBUG:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls',namespace='rest_framework')),
    ]
