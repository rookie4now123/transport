from django_filters import rest_framework as filters
from .models import LocationPoint

class LocationPointFilter(filters.FilterSet):

    route_name = filters.CharFilter(
        field_name='run__route__route_name', 
        lookup_expr='iexact'  # Case-insensitive exact match
    )

    date = filters.DateFilter(
        field_name='timestamp',
        lookup_expr='date'  # The '__date' lookup extracts the date part of a datetime
    )

    class Meta:
        model = LocationPoint
        # List the fields that this FilterSet will use.
        fields = ['route_name', 'date']