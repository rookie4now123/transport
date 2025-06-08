from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import viewsets
from .serializers import UserSerializer, MonitorSerializer
from .models import User, MonitorUser
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
        # This viewset should ONLY ever return Monitor Users
        return MonitorUser.objects.all()

    def get_serializer_class(self):
        # Use the create serializer for the 'create' action
        if self.action == 'create':
            return MonitorUserRegisterSerializer
        # Use the standard UserSerializer for all other actions (list, retrieve, etc.)
        return MonitorSerializer

    def get_object(self):
        obj = MonitorUser.objects.get_object_by_id(self.kwargs['pk'])
        self.check_object_permissions(self.request, obj)
        return obj