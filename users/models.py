from django.db import models
from django.contrib.auth.models import AbstractUser
from users.managers import CustomUserManager
from django.utils import timezone

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True, null=True)
    phone = models.CharField(max_length=11 ,blank=True, null=True)
    activation_token_created = models.DateTimeField(null=True, blank=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email' # email field will be used for authentication
    REQUIRED_FIELDS = [] # no required fields

    def __str__(self):
        return self.email

    def generate_activation_token(self):
        from users.utils import email_verification_token
        self.activation_token_created = timezone.now()
        self.save()
        return email_verification_token.make_token(self)