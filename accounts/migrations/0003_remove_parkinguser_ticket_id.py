# Generated by Django 4.2.16 on 2024-11-27 21:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_parkinguser_car_number_parkinguser_ticket_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='parkinguser',
            name='ticket_id',
        ),
    ]
