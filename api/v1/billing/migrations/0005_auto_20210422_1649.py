# Generated by Django 3.0.3 on 2021-04-22 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('billing', '0004_auto_20210421_0815'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='link',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='bill',
            name='qr_code',
            field=models.ImageField(blank=True, null=True, upload_to='qr_codes'),
        ),
    ]
