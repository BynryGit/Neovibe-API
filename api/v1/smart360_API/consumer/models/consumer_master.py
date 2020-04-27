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
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# Create Consumer Master table start.
class ConsumerMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email_id = models.CharField(max_length=200, null=True, blank=True)
    phone_no1 = models.CharField(max_length=200, null=True, blank=True)
    phone_no2 = models.CharField(max_length=200, null=True, blank=True)
    address_line_1 = models.CharField(max_length=500, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    country = models.IntegerField(null=True, blank=True)
    state = models.IntegerField(null=True, blank=True)
    city = models.IntegerField(null=True, blank=True)
    cycle = models.IntegerField(null=True, blank=True)
    area = models.IntegerField(null=True, blank=True)
    subarea = models.IntegerField(null=True, blank=True)
    route = models.IntegerField(null=True, blank=True)
    scheme = models.IntegerField(null=True, blank=True)
    deposit_amt = models.FloatField(null=True, blank=True)
    collected_amt = models.FloatField(null=True, blank=True)
    utility_service_plan = models.IntegerField(null=True, blank=True)  # TODO: Conform Foreignkey
    registration = models.CharField(null=True, blank=True)
    category = models.IntegerField(null=True, blank=True)
    sub_category = models.IntegerField(null=True, blank=True)
    is_vip = models.BooleanField(default=False)
    is_connectivity = models.BooleanField(default=False)
    gas_demand = models.CharField(null=True, blank=True)
    monthly_demand = models.CharField(null=True, blank=True)
    consumer_status = models.IntegerField(null=True, blank=True)
    consumption_ltd = models.CharField(null=True, blank=True)
    invoice_amount_ltd = models.CharField(null=True, blank=True)
    payment_ltd = models.CharField(null=True, blank=True)
    outstanding_ltd = models.CharField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.consumer_no

    def __unicode__(self):
        return self.consumer_no

# Create Consumer Master table end.
