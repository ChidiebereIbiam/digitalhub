from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.utils import timezone

class User(AbstractUser):
    username = models.CharField(max_length=250, null=True, blank=True)
    profile_image = models.ImageField(upload_to="profile_images/", null=True, blank=True)
    phone_number = models.CharField(max_length=250, null=True, blank=True)
    email = models.EmailField(max_length=254, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [
        'username',
        'first_name',
        'last_name'
    ]
    def __str__(self):
        return self.email
