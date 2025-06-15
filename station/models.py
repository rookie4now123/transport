from django.db import models
from core.abstract.models import AbstractModel, AbstractManager
from django.contrib.gis.db.models import PointField
from django.conf import settings
# Create your models here.

class StationManager(AbstractManager):
    pass
class Station(AbstractModel):
    station_name = models.CharField(db_index=True, max_length=100, unique=True)
    address = models.CharField(max_length=100, null = True)
    location = PointField(srid=settings.SRID_WGS84)
    
    creator = models.ForeignKey(
        'user.User',  # Reference your custom User model
        on_delete=models.SET_NULL,
        related_name='created_stations',
        null = True
    )
    
    objects = StationManager()

    def __str__(self):
        return f"{self.address}, {self.station_name}, {self.location}"
    class Meta:
        db_table = "station"