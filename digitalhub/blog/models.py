from django.db import models
from django.utils import timezone
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

def create_slug(title):
    slug = slugify(title)
    qs = Post.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        slug = "%s-%s" % (slug, qs.first().id)
    return slug

class Tag(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.TextField()
    slug = models.SlugField(null=True, blank=True, unique=True, max_length=255)
    header_image = models.ImageField(upload_to="blog_images/")
    body = RichTextField()
    conclusion = models.TextField()
    post_date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, null=True, blank=True)

    class Meta:
        ordering = ['-post_date']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = create_slug(self.title)
        return super().save(*args, **kwargs)


    
