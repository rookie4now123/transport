from rest_framework.permissions import BasePermission
from core.user.models import UserType

class IsWebUser(BasePermission):
    """
    Allows access only to authenticated users with the 'WEB' user type.
    """

    def has_permission(self, request, view):
        # Check if the user is authenticated and is a WEB user.
        return bool(
            request.user and
            request.user.is_authenticated and
            request.user.user_type == UserType.WEB
        )

class IsMonitorUser(BasePermission):
    """
    Custom permission to only allow users with the user_type 'MONITOR' to access an object.
    """

    def has_permission(self, request, view):
        """
        Check if the user is authenticated and is a monitor.
        This is called for list views or on entry to detail views.
        """
        # The user must be authenticated AND have the user_type 'MONITOR'
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.user_type == UserType.MONITOR)