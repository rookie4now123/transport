from django_filters import rest_framework as filters
from station.models import Station

class StationFilter(filters.FilterSet):
    # Example: Filter by exact station_name (case-insensitive)
    station_name = filters.CharFilter(field_name='station_name', lookup_expr='iexact')
    # Example: Filter by station_name containing a string (case-insensitive)
    station_name_contains = filters.CharFilter(field_name='station_name', lookup_expr='icontains')
    # Example: Filter by address containing a string
    address_contains = filters.CharFilter(field_name='address', lookup_expr='icontains')
    # You can add filters for other fields as well (DateFilter, NumberFilter, etc.)
    # created_after = filters.DateFilter(field_name='created', lookup_expr='gte')
    class Meta:
        model = Station
        fields = [
            'station_name', # For exact match (if not defined above with lookup_expr)
            'station_name_contains',
            'address_contains',
            # 'created_after'
        ]