# Generated by Django 5.0.3 on 2024-03-30 08:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interests', models.CharField(max_length=255)),
                ('phone_number', models.CharField(max_length=15)),
                ('address1', models.CharField(max_length=255)),
                ('address2', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('zipcode', models.CharField(max_length=10)),
                ('province', models.CharField(max_length=100)),
                ('billing_address1', models.CharField(max_length=255)),
                ('billing_address2', models.CharField(blank=True, max_length=255)),
                ('billing_city', models.CharField(max_length=100)),
                ('billing_zipcode', models.CharField(max_length=10)),
                ('billing_province', models.CharField(max_length=100)),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='profile_photos/')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
