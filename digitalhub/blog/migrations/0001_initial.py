# Generated by Django 5.0.6 on 2024-09-03 11:51

import ckeditor.fields
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('subtitle', models.TextField()),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('header_image', models.ImageField(upload_to='blog_images/')),
                ('body', ckeditor.fields.RichTextField()),
                ('conclusion', models.TextField()),
                ('post_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(to='blog.tag')),
            ],
            options={
                'ordering': ['-post_date'],
            },
        ),
    ]
