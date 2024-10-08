from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Company_Category(models.Model):
    name = models.CharField(max_length=250)
    
    class Meta:
        verbose_name = "Company Category"
        verbose_name_plural = "Company Categories"
    def __str__(self):
        return self.name

class Company(models.Model):
    company_name = models.CharField(max_length=250, unique=True)
    address = models.TextField()
    company_website = models.URLField(max_length=200)
    category = models.ForeignKey(Company_Category, on_delete=models.CASCADE)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"

    def __str__(self) -> str:
        return self.company_name  
    

class Preference(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_notification = models.BooleanField(default=True)
    browser_notification = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.user.email