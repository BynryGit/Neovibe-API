# Generated by Django 3.0.11 on 2021-03-17 03:06

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import fsm.fsm
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utility', '__first__'),
        ('tenant', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='RegistrationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('utility_product_id', models.BigIntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationSubType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('registration_type_id', models.BigIntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.CreateModel(
            name='RegistrationStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('state', models.BigIntegerField(choices=[(0, 'CREATED'), (1, 'APPROVED')], default=0)),
                ('ui_class', models.CharField(blank=True, max_length=200, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('state', models.BigIntegerField(choices=[(0, 'CREATED'), (1, 'APPROVED')], default=0)),
                ('registration_no', models.CharField(blank=True, max_length=200, null=True)),
                ('email_id', models.CharField(blank=True, max_length=200, null=True)),
                ('phone_mobile', models.CharField(blank=True, max_length=200, null=True)),
                ('phone_landline', models.CharField(blank=True, max_length=200, null=True)),
                ('billing_address_line_1', models.CharField(blank=True, max_length=200, null=True)),
                ('billing_street', models.CharField(blank=True, max_length=200, null=True)),
                ('billing_zipcode', models.CharField(blank=True, max_length=200, null=True)),
                ('billing_state_id', models.BigIntegerField(blank=True, null=True)),
                ('billing_city_id', models.BigIntegerField(blank=True, null=True)),
                ('billing_area_id', models.BigIntegerField(blank=True, null=True)),
                ('billing_sub_area_id', models.BigIntegerField(blank=True, null=True)),
                ('premise_id', models.BigIntegerField(blank=True, null=True)),
                ('credit_rating_id', models.BigIntegerField(blank=True, null=True)),
                ('registration_obj', django.contrib.postgres.fields.jsonb.JSONField(default='')),
                ('is_auto_pay', models.BooleanField(default=False)),
                ('is_loan', models.BooleanField(default=False)),
                ('is_upfront_amount', models.BooleanField(default=False)),
                ('ownership_id', models.BigIntegerField(blank=True, null=True)),
                ('is_address_same', models.BooleanField(default=False)),
                ('is_vip', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
            bases=(models.Model, fsm.fsm.FiniteStateMachineMixin),
        ),
    ]
