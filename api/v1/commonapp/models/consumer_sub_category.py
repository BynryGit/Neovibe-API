# Table Header
# module: S&M, Consumer Care & Ops | sub-module - Consumer, Metering, Billing, Payments, Services, Complaints
# Table Type : Lookup (Global)
# Table Name : 2.12.15 Consumer Sub-Category
# Description : It is a global lookup table that will store sub categories of consumers with respect to categories
# Frequency of data changes : Low
# Sample Table Data : "Builder" , "Individual"
# Reference Table : 2.2.2 Service Plans, 2.3.1 Survey Table, 2.3.8 Campaign Transaction Table,
#                    2.3.1. Consumer Master, 2.3.2. Consumer - Registration, 2.4.3 Asset Master, 2.7.1. Employee
# Author : Jayshree Kumbhare
# Creation Date : 21-04-2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime # importing package for datetime

from django.db import models  # importing package for database

# Create Consumer Sub Category table start
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster


class ConsumerSubCategory(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    category = models.BigIntegerField(blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Consumer Sub Category table end


def get_consumer_sub_category_by_id_string(id_string):
    return ConsumerSubCategory.objects.get(id_string = id_string)


def get_consumer_sub_category_by_id(id):
    return ConsumerSubCategory.objects.get(id = id)

# End the Code

