from rest_framework import serializers
from .models import User
from core.abstract.serializers import AbstractSerializer

class UserSerializer(AbstractSerializer):
    user_type = serializers.CharField(read_only=True)
    class Meta:
        model = User
        # List all fields from the base User model that you want to expose
        fields = [
            'id', 
            'username', 
            'email',
            'first_name',
            'last_name',
            'user_type'
        ]
        # Fields that should not be changed via the API
        read_only_fields = [
            #'is_active',
            'user_type',
        ]
