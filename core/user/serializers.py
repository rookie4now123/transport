from rest_framework import serializers
from .models import User
from core.abstract.serializers import AbstractSerializer

class UserSerializer(AbstractSerializer):

    class Meta:
        model = User
        # List of all the fields that can be included in a request or a response
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_active",
            "created",
            "updated",
        ]
        
        read_only_field = ['is_active']