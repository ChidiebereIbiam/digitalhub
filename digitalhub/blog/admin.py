from django.contrib import admin
from .models import Post, Tag
# Register your models here.

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title','author', 'post_date')

admin.site.register(Tag)