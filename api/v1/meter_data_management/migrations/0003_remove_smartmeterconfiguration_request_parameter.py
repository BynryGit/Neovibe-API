# Generated by Django 3.0.11 on 2021-03-18 09:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meter_data_management', '0002_remove_smartmeterconfiguration_description'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='smartmeterconfiguration',
            name='request_parameter',
        ),
    ]
