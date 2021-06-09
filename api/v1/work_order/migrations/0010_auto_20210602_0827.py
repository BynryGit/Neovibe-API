# Generated by Django 3.0.3 on 2021-06-02 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('work_order', '0009_merge_20210601_0900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serviceappointment',
            name='sa_description',
            field=models.CharField(blank=True, max_length=3000, null=True),
        ),
        migrations.AlterField(
            model_name='serviceappointment',
            name='state',
            field=models.BigIntegerField(choices=[(0, 'CREATED'), (1, 'NOT ASSIGNED'), (2, 'ASSIGNED'), (3, 'IN PROGRESS'), (4, 'FAILED'), (5, 'ACCEPTED'), (6, 'REJECTED'), (7, 'COMPLETED'), (8, 'HOLD'), (9, 'CLOSED'), (10, 'ARCHIVED'), (11, 'REQUESTED')], default=0),
        ),
        migrations.AlterField(
            model_name='serviceappointment',
            name='updated_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]