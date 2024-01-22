# user/models.py

from django.db import models
from django.contrib.auth.models import AbstractUser,BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractUser):
    USER_TYPES = (
        ('tourist', 'Tourist'),
        ('host', 'Host'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='tourist')
    email = models.EmailField(unique=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
