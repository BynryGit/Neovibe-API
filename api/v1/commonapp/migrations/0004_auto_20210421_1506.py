# Generated by Django 3.0.11 on 2021-04-21 09:36

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('commonapp', '0003_auto_20210416_1633'),
    ]

    operations = [
        migrations.AddField(
            model_name='document',
            name='auth_time_span',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='document_auth_details',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
        migrations.AddField(
            model_name='document',
            name='last_auth_generated',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True),
        ),
    ]
