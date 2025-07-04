from rest_framework import serializers
from django.contrib.gis.geos import Point
from .models import LocationPoint, RouteRun
from django.conf import settings
from route.models import Route
from django.utils import timezone
class RouteRunSerializer(serializers.ModelSerializer):
    # Use SlugRelatedField to show names in read operations
    monitor_name = serializers.SlugRelatedField(source='monitor', read_only=True, slug_field='username')
    route_name = serializers.SlugRelatedField(source='route', read_only=True, slug_field='route_name')
    route = serializers.PrimaryKeyRelatedField(
        queryset=Route.objects.all(), write_only=True
    )
    class Meta:
        model = RouteRun
        fields = ['id', 'route', 'monitor_name', 'route_name', 'end_time', 'status']
        # 'monitor' and 'start_time' will be set automatically by the view
        read_only_fields = ['monitor', 'end_time']

    def update(self, instance, validated_data):
        # Check if status is being set to COMPLETED
        status = validated_data.get('status', instance.status)
        if status == 'COMPLETED' and instance.end_time is None:
            instance.end_time = timezone.now()
        # Update the status (and any other fields)
        return super().update(instance, validated_data)

class LocationPointSerializer(serializers.ModelSerializer):
    # Keep latitude and longitude as write-only fields for input
    latitude = serializers.FloatField(write_only=True)
    longitude = serializers.FloatField(write_only=True)
    route_name = serializers.CharField(source='run__route__route_name', read_only=True)
    class Meta:
        model = LocationPoint
        # 'location' will be used for reading, lat/lon for writing
        fields = ['id', 'run', 'location', 'latitude', 'longitude', 'timestamp', 'route_name']
        read_only_fields = ['timestamp', 'location']

    def create(self, validated_data):
        # Extract lat/lon from the validated data
        lat = validated_data.pop('latitude')
        lon = validated_data.pop('longitude')

        # Create a Point object (longitude, latitude)
        validated_data['location'] = Point(lon, lat, srid=settings.SRID_WGS84)

        return super().create(validated_data)