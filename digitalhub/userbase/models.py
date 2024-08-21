from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Company(models.Model):
    name = models.CharField(max_length=250, unique=True)
    email = models.EmailField(max_length=254)
    address = models.TextField()
    phone = models.CharField(max_length=50)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self) -> str:
        return self.name 