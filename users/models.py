from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=11 ,blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email' # email field will be used for authentication
    REQUIRED_FIELDS = [] # no required fields

    def __str__(self):
        return self.email