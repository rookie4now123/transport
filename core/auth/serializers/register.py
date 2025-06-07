from rest_framework import serializers
from core.user.serializers import UserSerializer
from core.user.models import User

class RegisterSerializer(UserSerializer):
    password = serializers.CharField(max_length=64, min_length=6, write_only=True, required=True)
    class Meta:
        model = User
        fields = ['id', 'email',
                    'username', 'first_name', 'last_name','password'
                ]
    def create(self, validated_data):
        return User.objects.acreate_user(**validated_data)