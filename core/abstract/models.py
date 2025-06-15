from django.db import models
import uuid
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

class AbstractManager(models.Manager):
    def get_object_by_id(self, pk_id):
        try:
            return self.get(pk=pk_id)
        except (ObjectDoesNotExist, ValueError, TypeError):
            raise Http404("Object not found")

class AbstractModel(models.Model):
    id = models.UUIDField(db_index=True, unique=True, primary_key=True,
                          default=uuid.uuid4, editable=False)
    is_active = models.BooleanField(default=True, db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    objects = AbstractManager()
    
    class Meta:
        abstract = True