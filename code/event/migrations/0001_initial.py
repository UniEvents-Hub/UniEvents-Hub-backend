# Generated by Django 5.0.3 on 2024-03-30 08:38

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
            name='Event',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('event_type', models.CharField(default='music', max_length=100)),
                ('banner', models.ImageField(upload_to='event_banners/')),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('description', models.TextField()),
                ('ticket_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('ticket_type', models.CharField(max_length=50)),
                ('sharable_link', models.URLField()),
                ('address', models.CharField(max_length=255)),
                ('total_tickets', models.IntegerField()),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
