from rest_framework import serializers
from .models import MonitorUser, User
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
class MonitorSerializer(UserSerializer):
    class Meta:
        model = MonitorUser # Target the correct model
        
        fields = UserSerializer.Meta.fields + ['device_id']
        
        # We can also extend the read_only_fields if needed
        #read_only_fields = UserSerializer.Meta.read_only_fields + ['device_id']
        