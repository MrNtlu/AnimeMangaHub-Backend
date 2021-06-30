from django.shortcuts import render
from rest_framework.authtoken.views import ObtainAuthToken, AuthTokenSerializer
from rest_framework.settings import api_settings
from rest_framework.authtoken.models import Token
from src.base_response import handleResponseMessage
from rest_framework import status
from rest_framework.decorators import api_view

# Create your views here.
class LoginUser(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
            return handleResponseMessage(status.HTTP_200_OK,
                                         'Successfully logged in.',
                                         {
                                             "token": token.key,
                                             "id": user.pk
                                         })
        else:
            error_message = ""
            try:
                error_message = serializer.errors["non_field_errors"][0]
            except:
                error_message = "Unable to login. Please check credentials."
            return handleResponseMessage(status.HTTP_400_BAD_REQUEST,error_message)
        
@api_view(['GET'])
def test(request):
    if request.user.is_authenticated:
    
        return handleResponseMessage(
            status.HTTP_200_OK,
            'Successfully called')
    else:
        return handleResponseMessage(status.HTTP_401_UNAUTHORIZED,'Authentication error.')