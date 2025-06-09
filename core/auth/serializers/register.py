from rest_framework import serializers
from core.user.serializers import UserSerializer
from core.user.models import User, UserType

class RegisterSerializer(UserSerializer):
    password = serializers.CharField(max_length=64, min_length=6, write_only=True, required=True)
    class Meta:
        abstract = True # This makes sure this base class cannot be used directly
    def create(self, validated_data):
        raise NotImplementedError("Subclasses must implement this create method.")


class WebUserRegisterSerializer(RegisterSerializer):
    class Meta(RegisterSerializer.Meta):
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'user_type']
        read_only_fields = ['user_type']
    def create(self, validated_data):
        validated_data['user_type'] = UserType.WEB
        return User.objects.acreate_user(**validated_data)

class MonitorUserRegisterSerializer(RegisterSerializer):
    # Monitor users might not need first/last name, for example
    class Meta(RegisterSerializer.Meta):
        model = User
        fields = ['id', 'username', 'password','user_type']
        read_only_fields = ['user_type']
    def create(self, validated_data):
        validated_data['user_type'] = UserType.MONITOR
        return User.objects.acreate_user(**validated_data)