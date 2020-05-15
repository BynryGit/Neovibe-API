# Table Header
# Module: Consumer Care and Ops
# Table Type : Master
# Table Name : 2.4.1. Consumer Master
# Description :All active and inactive consumer for given tenant will be saved in this table all master values
# Frequency of data changes : High
# Sample table : Consumer 1, Consumer 2, Consumer 3, Consumer 4
# Reference Table : None
# Author : Jayshree Kumbhare
# Creation Date : 23/04/2020


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster

from django.db import models  # importing package for database


# Create Consumer Master table start.
class ConsumerMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email_id = models.CharField(max_length=200, null=True, blank=True)
    phone_mobile = models.CharField(max_length=200, null=True, blank=True)
    phone_landline = models.CharField(max_length=200, null=True, blank=True)
    address_line_1 = models.CharField(max_length=500, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.CharField(max_length=200, null=True, blank=True)
    country = models.BigIntegerField(null=True, blank=True)
    state = models.BigIntegerField(null=True, blank=True)
    city = models.BigIntegerField(null=True, blank=True)
    cycle = models.BigIntegerField(null=True, blank=True)
    area = models.BigIntegerField(null=True, blank=True)
    subarea = models.BigIntegerField(null=True, blank=True)
    route = models.BigIntegerField(null=True, blank=True)
    scheme = models.BigIntegerField(null=True, blank=True)
    deposit_amt = models.FloatField(null=True, blank=True)
    collected_amt = models.FloatField(null=True, blank=True)
    utility_service_plan = models.BigIntegerField(null=True, blank=True)  # TODO: Conform Foreignkey
    registration = models.CharField(max_length=200, null=True, blank=True)
    category = models.BigIntegerField(null=True, blank=True)
    sub_category = models.BigIntegerField(null=True, blank=True)
    is_vip = models.BooleanField(default=False)
    is_connectivity = models.BooleanField(default=False)
    gas_demand = models.CharField(max_length=200, null=True, blank=True)
    monthly_demand = models.CharField(max_length=200, null=True, blank=True)
    consumer_status = models.BigIntegerField(null=True, blank=True)
    consumption_ltd = models.CharField(max_length=200, null=True, blank=True)
    invoice_amount_ltd = models.CharField(max_length=200, null=True, blank=True)
    payment_ltd = models.CharField(max_length=200, null=True, blank=True)
    outstanding_ltd = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.consumer_no

    def __unicode__(self):
        return self.consumer_no

def get_consumer_by_id_string(id_string):
    try:
        return ConsumerMaster.objects.get(id_string = id_string)
    except Exception as e:
        return False

# Create Consumer Master table end.
