# Generated by Django 3.0.3 on 2021-03-26 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meter_data_management', '0007_uploadroute'),
    ]

    operations = [
        migrations.AddField(
            model_name='consumerdetail',
            name='state',
            field=models.IntegerField(choices=[(0, 'MANUAL'), (1, 'SMART')], default=0),
        ),
    ]
