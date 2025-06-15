from rest_framework import serializers
from django.db import transaction
from .models import Route, RouteSchedule, Station
from station.serializers import StationSerializer
from core.user.models import User  # Adjust import path
from core.user.serializers import UserSerializer # <--- IMPORT YOUR SERIALIZER

# This serializer is for *reading* the schedule data in a nested way
class RouteScheduleReadSerializer(serializers.ModelSerializer):
    station = StationSerializer(read_only=True)
    class Meta:
        model = RouteSchedule
        fields = ['id', 'station', 'day_of_week', 'time_of_day', 'arrival_time']

class RouteScheduleWriteSerializer(serializers.Serializer):
    # This will automatically validate that the input is a valid UUID
    # and that a Station with this ID exists.
    station = serializers.PrimaryKeyRelatedField(
        queryset=Station.objects.filter(is_active=True)
    )
    day_of_week = serializers.ChoiceField(choices=RouteSchedule.DAY_CHOICES)
    time_of_day = serializers.ChoiceField(choices=RouteSchedule.TIME_CHOICES)
    arrival_time = serializers.TimeField()
# This is the main serializer for the Route model
class RouteSerializer(serializers.ModelSerializer):
    schedule_entries = RouteScheduleReadSerializer(many=True, read_only=True)
    monitors = UserSerializer(many=True, read_only=True)
    monitors_ids = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(user_type='MONITOR'),
        many=True,
        write_only=True,
        source='monitors'
    )
    schedule_data = RouteScheduleWriteSerializer(many=True, write_only=True)

    class Meta:
        model = Route
        fields = [
            'id',
            'route_name',
            'monitors', # For reading
            'monitors_ids', # For writing
            'schedule_entries', # For reading
            'schedule_data', # For writing
        ]

    
    @transaction.atomic
    def create(self, validated_data):
        schedule_data = validated_data.pop('schedule_data')
        monitors = validated_data.pop('monitors')
        # Create the main Route object
        route = Route.objects.create(route_name=validated_data['route_name'])
        route.monitors.set(monitors)
        # Create the nested RouteSchedule objects
        for entry_data in schedule_data:
            RouteSchedule.objects.create(route=route, **entry_data)
        return route
    
    @transaction.atomic
    def update(self, instance, validated_data):
        """
        Handle updating a Route and its nested schedule.
        A simple approach is to delete the old schedule and create the new one.
        """
        # Pop the nested data
        schedule_data = validated_data.pop('schedule_data', None)
        monitors = validated_data.pop('monitors', None)

        # Update the simple fields on the Route instance
        instance.route_name = validated_data.get('route_name', instance.route_name)
        
        if monitors is not None:
            instance.monitors.set(monitors)
        
        if schedule_data is not None:
            # Delete existing schedule entries for this route
            instance.schedule_entries.all().delete()
            # Create the new schedule entries
            for entry_data in schedule_data:
                RouteSchedule.objects.create(route=instance, **entry_data)

        instance.save()
        return instance