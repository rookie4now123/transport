from django.db import models
from core.abstract.models import AbstractModel
from route.models import RouteSchedule # The key import!

class Student(AbstractModel):

    student_id = models.CharField(max_length=50, unique=True, db_index=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    
    grade = models.CharField(max_length=10, blank=True, null=True)
    class_name = models.CharField(max_length=10, blank=True, null=True, verbose_name="Class")

    is_bus_rider = models.BooleanField(default=True)

    # --- THE KEY PART ---
    # This single ForeignKey links the student to a specific, valid route-station pair.
    assignment = models.ForeignKey(
        RouteSchedule,
        on_delete=models.SET_NULL,  # If a schedule entry is deleted, the student becomes unassigned.
        null=True,                 # Allows a student to be unassigned.
        blank=True,                # Allows the field to be empty in forms.
        related_name="students",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    @property
    def assigned_route(self):
        """A helper property to easily get the student's assigned route."""
        if self.assignment:
            return self.assignment.route
        return None

    @property
    def assigned_station(self):
        """A helper property to easily get the student's assigned station."""
        if self.assignment:
            return self.assignment.station
        return None