from .models import Route
from .serializers import RouteSerializer
from rest_framework.permissions import IsAuthenticated
from core.auth.permissions import IsWebUser
from core.abstract.viewsets import AbstractViewSet
from core.filters import StationFilter
from rest_framework import viewsets, filters as drf_filters # Renamed to avoid clash
from django_filters import rest_framework as django_filter_backends # Specific import


class RouteViewSet(AbstractViewSet):
    """
    API endpoint for viewing and managing routes and their schedules.
    Handles nested creation and updates of schedules.
    """
    queryset = Route.objects.prefetch_related(
        'monitors', 
        'schedule_entries__station' # Important optimization!
    ).all()
    serializer_class = RouteSerializer
    permission_classes = (IsAuthenticated, IsWebUser)