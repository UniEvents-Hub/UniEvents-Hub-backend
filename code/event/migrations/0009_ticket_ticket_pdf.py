# Generated by Django 5.0.3 on 2024-04-07 22:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0008_event_total_tickets_remaining_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='ticket_pdf',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
