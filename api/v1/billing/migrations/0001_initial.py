# Generated by Django 3.0.10 on 2021-03-10 16:31

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('utility', '__first__'),
        ('tenant', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tax',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('tax_name', models.CharField(max_length=200)),
                ('tax_percentage', models.CharField(max_length=200)),
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
            name='ScheduleBillLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('schedule_bill_id', models.BigIntegerField()),
                ('bill_cycle_id', models.BigIntegerField()),
                ('recurring_id', models.BigIntegerField(blank=True, null=True)),
                ('utility_product_id', models.BigIntegerField(blank=True, null=True)),
                ('schedule_bill_log_status', models.IntegerField(choices=[(0, 'PENDING'), (1, 'COMPLETED'), (2, 'INPROGRESS')], default=0)),
                ('date_and_time', models.DateTimeField(blank=True, null=True)),
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
            name='ScheduleBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('bill_cycle_id', models.BigIntegerField(blank=True, null=True)),
                ('frequency_id', models.BigIntegerField(blank=True, null=True)),
                ('repeat_every_id', models.BigIntegerField(blank=True, null=True)),
                ('recurring_id', models.BigIntegerField(blank=True, null=True)),
                ('utility_product_id', models.BigIntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('occurs_on', django.contrib.postgres.fields.jsonb.JSONField(default=[])),
                ('cron_expression', models.CharField(blank=True, max_length=500, null=True)),
                ('schedule_status', models.IntegerField(choices=[(0, 'PENDING'), (1, 'COMPLETED'), (2, 'INPROGRESS')], default=0)),
                ('start_date', models.DateTimeField(blank=True, null=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
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
            name='Rate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('product_id', models.BigIntegerField(blank=True, null=True)),
                ('consumer_category_id', models.BigIntegerField(blank=True, null=True)),
                ('consumer_subcategory_id', models.BigIntegerField(blank=True, null=True)),
                ('unit', models.CharField(max_length=200)),
                ('rate', models.CharField(max_length=200)),
                ('start_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('end_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('is_fixted_rate', models.BooleanField(default=False)),
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
            name='InvoiceBill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('invoice_no', models.CharField(blank=True, max_length=200, null=True)),
                ('invoice_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('consumer_no', models.CharField(blank=True, max_length=200, null=True)),
                ('category_id', models.BigIntegerField(blank=True, null=True)),
                ('sub_category_id', models.BigIntegerField(blank=True, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('contact', models.CharField(blank=True, max_length=200, null=True)),
                ('conversion_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('consumer_status', models.CharField(blank=True, max_length=200, null=True)),
                ('cycle_id', models.BigIntegerField(blank=True, null=True)),
                ('route_id', models.BigIntegerField(blank=True, null=True)),
                ('utility_service_plan_id', models.BigIntegerField(blank=True, null=True)),
                ('bill_count', models.BigIntegerField(blank=True, null=True)),
                ('bill_month', models.CharField(blank=True, max_length=200, null=True)),
                ('due_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('meter_no', models.CharField(blank=True, max_length=200, null=True)),
                ('meter_status', models.BigIntegerField(blank=True, null=True)),
                ('meter_reading', models.BigIntegerField(blank=True, null=True)),
                ('previous_reading', models.FloatField(blank=True, null=True)),
                ('current_reading', models.FloatField(blank=True, null=True)),
                ('previous_reading_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('current_reading_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('consumption', models.FloatField(blank=True, null=True)),
                ('basic_price', models.FloatField(blank=True, null=True)),
                ('vat_percent', models.FloatField(blank=True, null=True)),
                ('total_price', models.FloatField(blank=True, null=True)),
                ('consumption_charges', models.FloatField(blank=True, null=True)),
                ('net_amount', models.FloatField(blank=True, null=True)),
                ('outstanding', models.FloatField(blank=True, null=True)),
                ('payment', models.FloatField(blank=True, null=True)),
                ('current_charges', models.FloatField(blank=True, null=True)),
                ('total_emi_paid', models.FloatField(blank=True, null=True)),
                ('remaining_emi_amt', models.FloatField(blank=True, null=True)),
                ('adjustments', models.CharField(blank=True, max_length=200, null=True)),
                ('before_due_date_amount', models.FloatField(blank=True, null=True)),
                ('after_due_date_amount', models.FloatField(blank=True, null=True)),
                ('current_emi_amt', models.FloatField(blank=True, null=True)),
                ('closing_month', models.CharField(blank=True, max_length=200, null=True)),
                ('bill_status_id', models.BigIntegerField(blank=True, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_adjusted', models.BooleanField(default=False)),
                ('is_spot_bill', models.BooleanField(default=False)),
                ('is_sms_send', models.BooleanField(default=False)),
                ('instruction_id', models.BigIntegerField(blank=True, null=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('is_active', models.BooleanField(default=False)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
        migrations.CreateModel(
            name='BillMonth',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('month', models.CharField(max_length=200)),
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
            name='BillFrequency',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('bill_frequency', models.BooleanField(default=False)),
                ('bill_period', models.CharField(max_length=200)),
                ('zone_id', models.BigIntegerField(blank=True, null=True)),
                ('area_id', models.BigIntegerField(blank=True, null=True)),
                ('city_id', models.BigIntegerField(blank=True, null=True)),
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
            name='BillCycle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('city_id', models.BigIntegerField(blank=True, null=True)),
                ('zone_id', models.BigIntegerField(blank=True, null=True)),
                ('division_id', models.BigIntegerField(blank=True, null=True)),
                ('area_id', models.BigIntegerField(blank=True, null=True)),
                ('subarea_id', models.BigIntegerField(blank=True, null=True)),
                ('utility_product_id', models.BigIntegerField(blank=True, null=True)),
                ('route_json', django.contrib.postgres.fields.jsonb.JSONField(default='')),
                ('label', models.CharField(blank=True, max_length=200, null=True)),
                ('bill_cycle_code', models.CharField(max_length=200)),
                ('bill_cycle_name', models.CharField(max_length=200)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
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
            name='BillConsumerDetail',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('consumer_id', models.BigIntegerField(blank=True, null=True)),
                ('meter_id', models.BigIntegerField(blank=True, null=True)),
                ('bill_schedule_log_id', models.BigIntegerField(blank=True, null=True)),
                ('bill_cycle_id', models.BigIntegerField(blank=True, null=True)),
                ('route_id', models.BigIntegerField(blank=True, null=True)),
                ('premise_id', models.BigIntegerField(blank=True, null=True)),
                ('utility_product_id', models.BigIntegerField(blank=True, null=True)),
                ('consumer_no', models.CharField(blank=True, max_length=200, null=True)),
                ('meter_no', models.CharField(blank=True, max_length=200, null=True)),
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
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('consumer_service_contract_detail_id', models.BigIntegerField(blank=True, null=True)),
                ('bill_cycle_id', models.BigIntegerField(blank=True, null=True)),
                ('bill_month', models.CharField(max_length=200)),
                ('bill_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('bill_period', models.CharField(max_length=200)),
                ('meter_reading', django.contrib.postgres.fields.jsonb.JSONField(default=[])),
                ('rate_details', django.contrib.postgres.fields.jsonb.JSONField(default=[])),
                ('additional_charges', django.contrib.postgres.fields.jsonb.JSONField(default=[])),
                ('opening_balance', models.CharField(max_length=200)),
                ('current_charges', models.CharField(max_length=200)),
                ('bill_frequency_id', models.BigIntegerField(blank=True, null=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_adjusted', models.BooleanField(default=False)),
                ('is_spot_bill', models.BooleanField(default=False)),
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
            name='AdditionalCharges',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('service_charges', models.CharField(max_length=200)),
                ('adjustment_amount', models.CharField(max_length=200)),
                ('penalty_charges', models.CharField(max_length=200)),
                ('discount_amount', models.CharField(max_length=200)),
                ('EMI', models.CharField(max_length=200)),
                ('rental_charges', models.CharField(max_length=200)),
                ('is_active', models.BooleanField(default=False)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('utility', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='utility.UtilityMaster')),
            ],
        ),
    ]
