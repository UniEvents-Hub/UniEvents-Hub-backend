# Generated by Django 5.0.3 on 2024-04-08 07:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0009_ticket_ticket_pdf'),
    ]

    operations = [
        migrations.CreateModel(
            name='ImageGallery',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('image', models.ImageField(blank=True, null=True, upload_to='gallery_images')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='event.event')),
            ],
        ),
    ]
