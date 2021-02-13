__author__ = "aki"

import uuid
from datetime import datetime
from django.db import models
from api.constants import get_file_name, METER_PICTURE
from v1.commonapp.models.global_lookup import get_global_lookup_by_id
from v1.commonapp.models.premises import get_premise_by_id
from v1.meter_data_management.models.route import get_route_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.contrib.postgres.fields import JSONField
from v1.utility.models.utility_product import get_utility_product_by_id


def get_file_path(instance, filename):
    return get_file_name(METER_PICTURE, filename)


class Meter(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    route_id = models.BigIntegerField(null=True, blank=True)
    premise_id = models.BigIntegerField(null=True, blank=True)
    category_id = models.BigIntegerField(null=True, blank=True)
    utility_product_id = models.BigIntegerField(null=True, blank=True)
    meter_type = models.BigIntegerField(null=True, blank=True)
    meter_no = models.CharField(max_length=200, blank=False, null=False)
    meter_make = models.CharField(max_length=200, blank=True, null=True)
    meter_image = models.FileField(upload_to=get_file_path, null=True, blank=True)
    initial_reading = models.CharField(max_length=200, blank=True, null=True)
    latitude = models.CharField(max_length=200, blank=True, null=True)
    longitude = models.CharField(max_length=200, blank=True, null=True)
    meter_detail = JSONField(default=[])
    install_date = models.DateTimeField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=True)

    @property
    def get_route_name(self):
        route = get_route_by_id(self.route_id)
        return route

    @property
    def get_premise_type(self):
        premise = get_premise_by_id(self.premise_id)
        return premise

    @property
    def get_category_name(self):
        category = get_global_lookup_by_id(self.category_id)
        return category

    @property
    def get_meter_type_name(self):
        meter_type = get_global_lookup_by_id(self.meter_type)
        return meter_type

    @property
    def get_utility_product_type_name(self):
        utility_product_type = get_utility_product_by_id(self.utility_product_id)
        return utility_product_type

    def __str__(self):
        return self.meter_make + ' ' + str(self.id_string)

    def __unicode__(self):
        return self.meter_make


def get_meter_by_id_string(id_string):
    try:
        return Meter.objects.get(id_string=id_string)
    except:
        return False


def get_meter_by_id(id):
    try:
        return Meter.objects.get(id=id)
    except:
        return False
