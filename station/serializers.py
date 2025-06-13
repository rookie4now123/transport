from core.abstract.serializers import AbstractSerializer
from .models import Station
from django.contrib.gis.geos import Point
from rest_framework import serializers

class StationSerializer(AbstractSerializer):
    creator = serializers.CharField(
        source='creator.username', 
        read_only=True  # Ensure the field is read-only
    )
    class Meta:
        model = Station
        fields = ['id', 'address', 'location', 
                  'creator',
                  'station_name']
        read_only_fields = ['creator']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        # Extract location coordinates
        if instance.location:
            data['location'] = {
                'latitude': instance.location.y,
                'longitude': instance.location.x
            }
        else:
            data['location'] = None
        return data

    def to_internal_value(self, data):
        location_data = data.get('location')
        if location_data and isinstance(location_data, dict):
            latitude = location_data.get('latitude')
            longitude = location_data.get('longitude')
            if latitude is not None and longitude is not None:
                try:
                    geos_point = Point(float(longitude), float(latitude), srid=4326)
                    mutable_data = data.copy() # Make a mutable copy
                    mutable_data['location'] = geos_point
                    return super().to_internal_value(mutable_data)
                
                except (ValueError, TypeError) as e:
                    raise serializers.ValidationError({
                        'location': f"Invalid latitude or longitude value: {e}"
                    })
            elif latitude is None and longitude is None and self.Meta.model._meta.get_field('location').null:
                pass
            else:
                raise serializers.ValidationError({
                    'location': "Both latitude and longitude are required if location is provided."
                })
            
        return super().to_internal_value(data)