from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from core.abstract.models import AbstractModel, AbstractManager

class UserType(models.TextChoices):
    WEB = "WEB", "Web"
    MONITOR = "MONITOR", "Monitor"
    PARENT = "PARENT", "Parent"

class UserManager(BaseUserManager, AbstractManager):
    def acreate_user(self, username, user_type, email=None, password=None, **kwargs):
        if username is None:
            raise TypeError('Users must have a username.')
        if password is None:
            raise TypeError('User must have an password.')
        if email:
            email = self.normalize_email(email)
        else:
            email = None # Explicitly set to None for the database
        if not user_type:
            raise TypeError('User must have a user_type.')
        #user_type = kwargs.pop('user_type', None)      
        # if user_type is None:
        #     raise TypeError('User must have a user_type.')
        user = self.model(username=username, email=email,
                          user_type=user_type,
                           **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def acreate_superuser(self, username, password , email = None,
                           **kwargs):
        """
        Create and return a `User` with superuser (admin)
        permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        if username is None:
            raise TypeError('Superusers must have an username.')

        user = self.acreate_user(username, password, email, **kwargs)
        user.save(using=self._db)
        return user
    
class User(AbstractModel, AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(db_index=True, unique=True, null = True)
    user_type = models.CharField(max_length=50, choices=UserType.choices)
    is_superuser = models.BooleanField(default=False)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['user_type']
    objects = UserManager()
    def __str__(self):
        return f"{self.username} ({self.user_type})"
    
    @property
    def name(self):
        return f"{self.first_name} {self.last_name}"
