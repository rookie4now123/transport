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