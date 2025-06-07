from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from core.user.serializers import UserSerializer
from core.user.models import User, UserType

class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except AuthenticationFailed:
            raise AuthenticationFailed(
                detail="Login failed. Please check your username and password and try again.", # Your custom message
                code="authentication_failed" # Optional: a custom error code
            )
        self.check_user_type()
        refresh = self.get_token(self.user)
        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)
        
        return data
    
    def check_user_type(self):
        """
        Hook for subclasses to implement user type validation.
        """
        raise NotImplementedError("Subclasses must implement this method.")

class WebUserLoginSerializer(LoginSerializer):
    def check_user_type(self):
        if self.user.user_type != UserType.WEB:
            raise AuthenticationFailed(
                detail="Monitor authentication failed.",
                code="authentication_failed"
            )

class MonitorUserLoginSerializer(LoginSerializer):
    def check_user_type(self):
        if self.user.user_type != UserType.MONITOR:
            raise AuthenticationFailed(
                detail="Authentication failed. This endpoint is for monitor users only.",
                code="authentication_failed"
            )