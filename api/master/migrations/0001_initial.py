# Generated by Django 3.0.3 on 2021-03-08 05:46

import datetime
from django.db import migrations, models
import django.db.models.deletion
import fsm.fsm
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
        ('tenant', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_string', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('user_id', models.CharField(blank=True, max_length=200, null=True)),
                ('city_id', models.BigIntegerField(blank=True, null=True)),
                ('user_type_id', models.BigIntegerField(blank=True, null=True)),
                ('user_subtype_id', models.BigIntegerField(blank=True, null=True)),
                ('form_factor_id', models.BigIntegerField(blank=True, null=True)),
                ('department_id', models.BigIntegerField(blank=True, null=True)),
                ('status_id', models.BigIntegerField(blank=True, null=True)),
                ('state', models.BigIntegerField(choices=[(0, 'CREATED'), (1, 'ACTIVE'), (2, 'INACTIVE'), (3, 'ARCHIVED')], default=0)),
                ('password', models.CharField(max_length=200, verbose_name='password')),
                ('first_name', models.CharField(blank=True, max_length=200)),
                ('middle_name', models.CharField(blank=True, max_length=200)),
                ('last_name', models.CharField(blank=True, max_length=200)),
                ('email', models.CharField(max_length=200, unique=True)),
                ('user_image', models.URLField(blank=True, null=True)),
                ('phone_mobile', models.CharField(blank=True, max_length=200, null=True)),
                ('phone_landline', models.CharField(blank=True, max_length=200, null=True)),
                ('supplier_id', models.BigIntegerField(blank=True, null=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('is_superuser', models.BooleanField(default=False)),
                ('last_login', models.DateTimeField(blank=True, null=True)),
                ('date_joined', models.DateTimeField(blank=True, null=True)),
                ('created_by', models.BigIntegerField(blank=True, null=True)),
                ('updated_by', models.BigIntegerField(blank=True, null=True)),
                ('created_date', models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 16, 42, 168406), null=True)),
                ('updated_date', models.DateTimeField(blank=True, default=datetime.datetime(2021, 3, 8, 11, 16, 42, 168406), null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('tenant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='tenant.TenantMaster')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, fsm.fsm.FiniteStateMachineMixin),
        ),
    ]
