from rest_framework import viewsets, permissions, filters
from .models import Student
from .serializers import StudentSerializer
from core.auth.permissions import IsWebUser # Use an appropriate permission for admins

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    # This endpoint should likely only be accessible by admins/staff.
    permission_classes = [permissions.IsAuthenticated, IsWebUser]
    queryset = Student.objects.select_related(
        'assignment__route', 
        'assignment__station'
    ).all()

    # --- Filtering, Searching, and Ordering Configuration ---
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        # DjangoFilterBackend must be explicitly named here if also default
    ]
    # Fields to be used with the `?search=` parameter
    search_fields = ['student_id', 'first_name', 'last_name']
    ordering_fields = ['student_id', 'last_name', 'first_name', 'grade', 'is_bus_rider']
    filterset_fields = ['grade', 'class_name', 'is_bus_rider', 'assignment__route__id', 'assignment__station__id']