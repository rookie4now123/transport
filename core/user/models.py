import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.http import Http404
from core.abstract.models import AbstractModel, AbstractManager

class UserType(models.TextChoices):
    WEB = "WEB", "Web"
    MONITOR = "MONITOR", "Monitor"

class UserManager(BaseUserManager, AbstractManager):
    def get_object_by_id(self, pk_id):
        try:
            return self.get(pk=pk_id)
        except (ObjectDoesNotExist, ValueError, TypeError):
            return Http404
    def acreate_user(self, username, email=None, password=None, **kwargs):
        if username is None:
            raise TypeError('Users must have a username.')
        if password is None:
            raise TypeError('User must have an email.')
        if email:
            email = self.normalize_email(email)
        else:
            email = None # Explicitly set to None for the database
        #user_type = kwargs.pop('user_type', None)      
        # if user_type is None:
        #     raise TypeError('User must have a user_type.')
 
        user = self.model(username=username, email=email,
                           **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def acreate_superuser(self, username, email = None, password = None,
                           **kwargs):
        """
        Create and return a `User` with superuser (admin)
        permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        if username is None:
            raise TypeError('Superusers must have an username.')

        user = self.acreate_user(username, email, password, **kwargs)
        user.save(using=self._db)
        return user
    
class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True, null = True)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['user_type']
    objects = UserManager()
    def __str__(self):
        return f"{self.email}"
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def user_type(self):
        # If a related monitoruser object exists, it's a MonitorUser.
        # Otherwise, it's a WebUser.
        if hasattr(self, 'monitoruser'):
            return UserType.MONITOR
        return UserType.WEB

class MonitorUser(User):
    # This inherits from User, creating a OneToOne link
    device_id = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = "Monitor User"