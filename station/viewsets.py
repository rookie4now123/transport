from rest_framework.permissions import IsAuthenticated
from .serializers import StationSerializer
from .models import Station
from core.auth.permissions import IsWebUser
from core.abstract.viewsets import AbstractViewSet
from core.filters import StationFilter
from rest_framework import viewsets, filters as drf_filters # Renamed to avoid clash
from django_filters import rest_framework as django_filter_backends # Specific import

class StationViewSet(AbstractViewSet):
    permission_classes = (IsAuthenticated, IsWebUser)
    http_method_names = ('get', 'post', 'patch', 'delete')
    serializer_class = StationSerializer
    def get_queryset(self):
        return Station.objects.all()
    filter_backends = AbstractViewSet.filter_backends + [django_filter_backends.DjangoFilterBackend]
    filterset_class = StationFilter # Tell DRF to use your StationFilter

    def perform_create(self, serializer):
        # Automatically set the creator to the current user
        serializer.save(creator=self.request.user)
        
    def get_permissions(self):
        if self.action == 'create':
            return [IsAuthenticated(), IsWebUser()]
        return super().get_permissions()