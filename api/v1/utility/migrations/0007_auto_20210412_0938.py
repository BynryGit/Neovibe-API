# Generated by Django 3.0.11 on 2021-04-12 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utility', '0006_auto_20210410_1638'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilityservicecontractmaster',
            name='duration',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='utilityservicecontractmaster',
            name='terms',
            field=models.CharField(blank=True, max_length=1000, null=True),
        ),
    ]