from rest_framework import serializers
from .models import Student
from route.models import RouteSchedule # Import the model we are linking to

# --- Helper Serializer for Reading the Assignment ---
# This serializer turns a RouteSchedule object into a detailed, readable dictionary.
class StudentAssignmentSerializer(serializers.ModelSerializer):
    route_name = serializers.CharField(source='route.route_name', read_only=True)
    station_name = serializers.CharField(source='station.station_name', read_only=True)

    class Meta:
        model = RouteSchedule
        fields = [
            'id', 
            'route_name', 
            'station_name', 
            'day_of_week', 
            'time_of_day', 
            'arrival_time'
        ]


# --- Main Serializer for the Student Model ---
class StudentSerializer(serializers.ModelSerializer):
    # For READING: Use the nested serializer to show full assignment details.
    # The `source='assignment'` tells DRF to use the 'assignment' field on the Student model.
    # `read_only=True` means this field will only be used for output.
    assignment_details = StudentAssignmentSerializer(source='assignment', read_only=True)

    # For WRITING: Accept a simple UUID to make an assignment.
    # `write_only=True` means this field will only be used for input.
    # `allow_null=True` is crucial to allow un-assigning a student.
    assignment_id = serializers.PrimaryKeyRelatedField(
        queryset=RouteSchedule.objects.all(),
        source='assignment',
        write_only=True,
        allow_null=True,
        required=False # Makes the field optional during creation/update
    )

    class Meta:
        model = Student
        fields = [
            'id',
            'student_id',
            'first_name',
            'last_name',
            'grade',
            'class_name',
            'is_bus_rider',
            'assignment_details', # For reading
            'assignment_id',      # For writing
        ]