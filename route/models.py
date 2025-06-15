from django.db import models
from core.abstract.models import AbstractModel
from core.user.models import User  # Adjust import path as needed
from station.models import Station  # Adjust import path as needed

# The new "through" model
class RouteSchedule(AbstractModel):
    route = models.ForeignKey(
                    'Route', 
                    on_delete=models.CASCADE,
                    related_name='schedule_entries')
    station = models.ForeignKey(
                    Station, 
                    on_delete=models.PROTECT,
                    related_name='schedule_appearances'
                    )
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
    ]
    day_of_week = models.CharField(max_length=3, choices=DAY_CHOICES)

    TIME_CHOICES = [
        ('AM', 'Morning'),
        ('PM', 'Afternoon'),
    ]
    time_of_day = models.CharField(max_length=2, choices=TIME_CHOICES)

    # The arrival time for this specific station on this day/time
    arrival_time = models.TimeField()

    class Meta:
        # Prevent creating the exact same schedule entry twice
        unique_together = ('route', 'station', 'day_of_week', 'time_of_day')
        # Order the schedule logically when querying
        ordering = ['day_of_week', 'arrival_time']

    def __str__(self):
        return (f"{self.route.route_name} -> {self.station.station_name} "
                f"({self.get_day_of_week_display()} {self.get_time_of_day_display()}) at {self.arrival_time}")

class Route(AbstractModel):
    route_name = models.CharField(max_length=100, unique=True, db_index=True)
    stations = models.ManyToManyField(
        Station,
        through='RouteSchedule',  # This is the key part!
        related_name='routes',
        blank = True
    )

    monitors = models.ManyToManyField(
        User,
        related_name='monitor_routes',
        limit_choices_to={'user_type': 'MONITOR'},
        blank=True
    )

    def __str__(self):
        return self.route_name