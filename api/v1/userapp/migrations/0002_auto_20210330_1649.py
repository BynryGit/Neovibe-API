# Generated by Django 3.0.11 on 2021-03-30 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrole',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
    ]