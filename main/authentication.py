
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from .models import CustomUser

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get('Authorization')
        if not token:
            return None

     
        try:
            user = CustomUser.objects.get(auth_token=token)
        except CustomUser.DoesNotExist:
            raise AuthenticationFailed('Invalid token or user does not exist')

        return (user, None)
