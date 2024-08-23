from django.db import models
from ckeditor.fields import RichTextField



class BundlePlan(models.Model):
    title = models.CharField(max_length=250)
    features = RichTextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.title} | {self.price}"


class StandAlonePlan(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.title