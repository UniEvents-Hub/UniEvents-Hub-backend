# Generated by Django 5.0.3 on 2024-04-01 07:39

import event.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0003_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to=event.models.upload_to),
        ),
    ]