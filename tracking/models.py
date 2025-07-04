from django.db import models
from core.abstract.models import AbstractModel
from core.user.models import User
from route.models import Route
from django.conf import settings
from django.contrib.gis.db.models import PointField
class RouteRun(AbstractModel):
    """
    Represents a single, specific instance of a monitor running a route.
    This is the "session" or "trip".
    """
    STATUS_CHOICES = [
        ('IN_PROGRESS', 'In Progress'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]

    route = models.ForeignKey(Route, on_delete=models.PROTECT)
    monitor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        limit_choices_to={'user_type': 'MONITOR'}
    )
    end_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='IN_PROGRESS')

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return f"{self.route.route_name} run by {self.monitor.username} at {self.created.strftime('%Y-%m-%d %H:%M')}"

class LocationPoint(AbstractModel):
    """
    Represents a single GPS coordinate point recorded during a RouteRun.
    """
    run = models.ForeignKey(RouteRun, on_delete=models.CASCADE, related_name='location_points')
    
    # Use DecimalField for precision. Floats can have rounding errors.
    location = PointField(srid=settings.SRID_WGS84)

    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['timestamp']

    def __str__(self):
        return f"Point ({self.location.y:.4f}, {self.location.x:.4f}) for run {self.run.id} at {self.timestamp}"