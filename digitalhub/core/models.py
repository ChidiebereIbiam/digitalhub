from django.db import models
from ckeditor.fields import RichTextField
from django.template.defaultfilters import slugify


# Create your models here.
class Plan(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.title} | {self.price}"

class Benefit(models.Model):
    title = models.CharField(max_length=250)
    description = models.TextField()

    def __str__(self):
        return self.title    
class Service(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(null=True, blank=True, unique=True, max_length=255)
    header_image = models.ImageField(upload_to="service_images/")
    benefit = models.ForeignKey(Benefit, on_delete=models.CASCADE, related_name='services')
    description = RichTextField()
    bottom_image = models.ImageField(upload_to="service_images/")
    plans = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='services')

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug(self.title)
        return super().save(*args, **kwargs)


def create_slug(title):
    slug = slugify(title)
    qs = Service.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        slug = "%s-%s" % (slug, qs.first().id)
    return slug