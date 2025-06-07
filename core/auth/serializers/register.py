from rest_framework import serializers
from core.user.serializers import UserSerializer
from core.user.models import User, UserType

class RegisterSerializer(UserSerializer):
    password = serializers.CharField(max_length=64, min_length=6, write_only=True, required=True)
    class Meta:
        model = User
        fields = ['id',
                    'username', 'first_name', 'last_name','password'
                ]
    def create(self, validated_data):
        raise NotImplementedError("Subclasses must implement this method.")


class WebUserRegisterSerializer(RegisterSerializer):
    def create(self, validated_data):
        # Explicitly set the user_type for web users
        validated_data['user_type'] = UserType.WEB
        return User.objects.acreate_user(**validated_data)

class MonitorUserRegisterSerializer(RegisterSerializer):
    # Monitor users might not need first/last name, for example
    class Meta(RegisterSerializer.Meta):
        fields = ['id', 'email', 'username', 'password']

    def create(self, validated_data):
        # Explicitly set the user_type for monitor users
        validated_data['user_type'] = UserType.MONITOR
        return User.objects.acreate_user(**validated_data)