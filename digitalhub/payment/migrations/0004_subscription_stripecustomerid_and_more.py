# Generated by Django 5.0.6 on 2024-09-10 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_alter_standaloneplan_duration_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='stripeCustomerId',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='subscription',
            name='stripeSubscriptionId',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
