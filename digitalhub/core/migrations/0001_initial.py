# Generated by Django 5.0.6 on 2024-08-21 08:03

import ckeditor.fields
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Benefit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('slug', models.SlugField(blank=True, max_length=255, null=True, unique=True)),
                ('header_image', models.ImageField(upload_to='service_images/')),
                ('description', ckeditor.fields.RichTextField()),
                ('bottom_image', models.ImageField(upload_to='service_images/')),
                ('benefit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='core.benefit')),
                ('plans', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='core.plan')),
            ],
        ),
    ]
