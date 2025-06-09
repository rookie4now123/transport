from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from .serializers import UserSerializer
from .models import User, UserType
from core.auth.permissions import IsWebUser
from core.abstract.viewsets import AbstractViewSet
from core.auth.serializers.register import MonitorUserRegisterSerializer

class UserViewSet(AbstractViewSet):
    http_method_names = ('patch', 'get')
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)
    def get_object(self):
        obj = User.objects.get_object_by_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

class MonitorUserViewSet(AbstractViewSet):

    permission_classes = (IsAuthenticated, IsWebUser)
    http_method_names = ('get', 'post', 'patch', 'delete')
    def get_queryset(self):
        # FIXED: Instead of querying a separate model, we filter the main User model.
        return User.objects.filter(user_type=UserType.MONITOR)
    def get_serializer_class(self):
        # Use the specific creation serializer for the 'create' action
        if self.action == 'create':
            # Use the correctly named Create serializer
            return MonitorUserRegisterSerializer
        # For ALL other actions (list, retrieve, etc.), use the unified UserSerializer
        return UserSerializer

    def get_object(self):
        # Fetch from the main User model using the public_id
        obj = User.objects.get_object_by_public_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj

# class ParentUserViewSet(AbstractViewSet):
#     """
#     ViewSet for WebUsers to manage users of type PARENT.
#     """
#     permission_classes = (IsAuthenticated, IsWebUser)
#     http_method_names = ('get', 'post', 'patch', 'delete')

#     def get_queryset(self):
#         # Filter the main User model for parents
#         return User.objects.filter(user_type=UserType.PARENT)

#     def get_serializer_class(self):
#         if self.action == 'create':
#             return ParentUserCreateSerializer
#         return UserSerializer

#     def get_object(self):
#         obj = User.objects.get_object_by_public_id(self.kwargs['pk'])
#         self.check_object_permissions(self.request, obj)
#         return obj