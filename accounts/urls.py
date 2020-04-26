from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('accounts/', UserRegistrationAPIView.as_view(), name="list"), #POST
    path('accounts/login/', UserLoginAPIView.as_view(), name="login"), #POST
    path('tokens/<key>/', UserTokenAPIView.as_view(), name="token"), #GET, DELETE
]