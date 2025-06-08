from rest_framework import serializers
from core.user.serializers import UserSerializer
from core.user.models import User, UserType, MonitorUser

class RegisterSerializer(UserSerializer):
    password = serializers.CharField(max_length=64, min_length=6, write_only=True, required=True)
    class Meta:
        abstract = True # This makes sure this base class cannot be used directly
    def create(self, validated_data):
        raise NotImplementedError("Subclasses must implement this create method.")


class WebUserRegisterSerializer(RegisterSerializer):
    class Meta(RegisterSerializer.Meta):
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'password']
    def create(self, validated_data):
        return User.objects.acreate_user(**validated_data)

class MonitorUserRegisterSerializer(RegisterSerializer):
    # Monitor users might not need first/last name, for example
    class Meta(RegisterSerializer.Meta):
        model = MonitorUser
        fields = ['id', 'username', 'password']

    def create(self, validated_data):
        return MonitorUser.objects.acreate_user(**validated_data)