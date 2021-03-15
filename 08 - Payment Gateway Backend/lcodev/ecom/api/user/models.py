from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class CustomUser(AbstractUser):
    name = models.CharField(max_length=50, default='Anonymous')
    email = models.EmailField(max_length=254, unique=True)

    # The field is already there, we have to make it as None because we're not
    # going to be sign in of the user based on the username
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    phone = models.CharField(max_length=20, blank=True, null=True)
    gender = models.CharField(max_length=10, blank=True, null=True)

    # Django doesn't work wih token based so obviously the fields need to be
    # stored.
    session_token = models.CharField(max_length=10, default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
