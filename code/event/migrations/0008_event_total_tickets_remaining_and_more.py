# Generated by Django 5.0.3 on 2024-04-07 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('event', '0007_ticket_invoice_id_ticket_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='total_tickets_remaining',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='total_tickets_sold',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]