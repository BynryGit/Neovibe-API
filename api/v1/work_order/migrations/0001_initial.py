# Generated by Django 3.0.3 on 2021-04-19 07:28

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import fsm.fsm
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tenant', '__first__'),
        ('utility', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='WorkOrderRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('rule_id', models.BigIntegerField(blank=True, null=True)),
                ('rule', models.CharField(max_length=200)),
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
            name='WorkOrderMaster',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('work_order_number', models.BigIntegerField(blank=True, null=True)),
                ('utility_product_id', models.BigIntegerField(blank=True, null=True)),
                ('utility_work_order_type_id', models.BigIntegerField(blank=True, null=True)),
                ('utility_work_order_sub_type_id', models.BigIntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('json_obj', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('service_obj', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('base_rate', models.FloatField(blank=True, null=True)),
                ('tax_rate', models.FloatField(blank=True, null=True)),
                ('is_taxable', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceAssignment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('sa_id', models.BigIntegerField(blank=True, null=True)),
                ('user_id', models.BigIntegerField(blank=True, null=True)),
                ('state', models.BigIntegerField(choices=[(0, 'CREATED'), (1, 'NOT ASSIGNED'), (2, 'ASSIGNED'), (3, 'COMPLETED'), (4, 'HOLD'), (5, 'CLOSED'), (6, 'ARCHIVED')], default=1)),
                ('assignment_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('assignment_time', models.TimeField(blank=True, null=True)),
                ('completion_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('completion_time', models.TimeField(blank=True, null=True)),
                ('TAT', models.BigIntegerField(blank=True, null=True)),
                ('remark', models.CharField(blank=True, max_length=200, null=True)),
                ('status_id', models.BigIntegerField(blank=True, null=True)),
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
        migrations.CreateModel(
            name='ServiceAppointmentStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('status', models.CharField(max_length=200)),
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
            name='ServiceAppointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('consumer_service_contract_detail_id', models.BigIntegerField(blank=True, null=True)),
                ('asset_id', models.BigIntegerField(blank=True, null=True)),
                ('work_order_master_id', models.BigIntegerField(blank=True, null=True)),
                ('state', models.BigIntegerField(choices=[(0, 'CREATED'), (1, 'NOT ASSIGNED'), (2, 'ASSIGNED'), (3, 'IN PROGRESS'), (4, 'FAILED'), (5, 'ACCEPTED'), (6, 'REJECTED'), (7, 'COMPLETED'), (8, 'HOLD'), (9, 'CLOSED'), (10, 'ARCHIVED'), (11, 'REQUESTED')], default=1)),
                ('sa_number', models.CharField(blank=True, max_length=200, null=True)),
                ('sa_name', models.CharField(blank=True, max_length=200, null=True)),
                ('sa_description', models.CharField(blank=True, max_length=200, null=True)),
                ('sa_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('sa_estimated_effort', models.BigIntegerField(blank=True, null=True)),
                ('sa_rule', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('sa_user_remark', models.CharField(blank=True, max_length=200, null=True)),
                ('alternative_contact', models.CharField(blank=True, max_length=200, null=True)),
                ('address_line_1', models.CharField(blank=True, max_length=200, null=True)),
                ('street', models.CharField(blank=True, max_length=200, null=True)),
                ('zipcode', models.CharField(blank=True, max_length=200, null=True)),
                ('state_id', models.BigIntegerField(blank=True, null=True)),
                ('city_id', models.BigIntegerField(blank=True, null=True)),
                ('area_id', models.BigIntegerField(blank=True, null=True)),
                ('sub_area_id', models.BigIntegerField(blank=True, null=True)),
                ('premise_id', models.BigIntegerField(blank=True, null=True)),
                ('actual_start_time', models.TimeField(blank=True, default='20:00', null=True)),
                ('actual_end_time', models.TimeField(blank=True, default='20:00', null=True)),
                ('actual_duration', models.BigIntegerField(blank=True, null=True)),
                ('completed_task_details', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('sa_GIS_id', models.BigIntegerField(blank=True, null=True)),
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
        migrations.CreateModel(
            name='ScheduledAppointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('appointments', django.contrib.postgres.fields.jsonb.JSONField()),
                ('user_id', models.BigIntegerField(blank=True, null=True)),
                ('assignment_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
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
            name='MaterialType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=200)),
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
            name='MaterialSubType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('material_type_id', models.BigIntegerField(blank=True, null=True)),
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
            name='MaterialName',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('name', models.CharField(max_length=200)),
                ('material_subtype_id', models.BigIntegerField(blank=True, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
    ]
