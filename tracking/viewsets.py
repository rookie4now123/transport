from rest_framework import viewsets, mixins
from .models import RouteRun, LocationPoint
from .serializers import RouteRunSerializer, LocationPointSerializer
from rest_framework.permissions import IsAuthenticated
from core.auth.permissions import IsWebUser, IsMonitorUser

class MobileRouteRunViewSet(mixins.CreateModelMixin,
                             mixins.UpdateModelMixin, # For PATCH to end the run
                             viewsets.GenericViewSet):
    """
    Mobile-only endpoint for monitors to START and END a run.
    No listing or deleting is allowed.
    """
    queryset = RouteRun.objects.all()
    serializer_class = RouteRunSerializer
    permission_classes = [IsAuthenticated, IsMonitorUser]

    def perform_create(self, serializer):
        # Automatically set the monitor to the logged-in user
        serializer.save(monitor=self.request.user)


class MobileLocationPointViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Mobile-only endpoint for monitors to UPLOAD location points.
    """
    queryset = LocationPoint.objects.all()
    serializer_class = LocationPointSerializer
    permission_classes = [IsMonitorUser]
        
class WebRouteRunViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         viewsets.GenericViewSet):
    """
    Web-only, read-only endpoint for admins to VIEW all route runs.
    """
    queryset = RouteRun.objects.prefetch_related('monitor', 'route').all()
    serializer_class = RouteRunSerializer
    permission_classes = [IsWebUser]

class WebLocationPointViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    Web-only, read-only endpoint for admins to VIEW location points for a run.
    """
    serializer_class = LocationPointSerializer
    permission_classes = [IsWebUser]

    def get_queryset(self):
        # Allow filtering by run_id in the URL query params
        # e.g., /api/web/locationpoints/?run=...
        queryset = LocationPoint.objects.all()
        run_id = self.request.query_params.get('run')
        if run_id:
            return queryset.filter(run_id=run_id)
        return queryset