# Table Header
# module: S&M, Consumer Care & Ops | sub-module - Consumer, Metering, Billing, Payments, Services, Complaints
# Table Type : Lookup (Global)
# Table Name : 2.12.14 Consumer Category
# Description : It is a global lookup table that stores the various categories of consumers
# Frequency of data changes : Low
# Sample Table Data : "Domestic"
# Reference Table : 2.2.2 Service Plans, 2.3.1 Survey Table, 2.3.8 Campaign Transaction Table,
#                    2.3.1. Consumer Master, 2.3.2. Consumer - Registration, 2.4.3 Asset Master, 2.7.1. Employee.
# Author : Jayshree Kumbhare
# Creation Date : 21/04/2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Consumer Category table start



class ConsumerCategory(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=True, null=True)
    service_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Consumer Category table end

def get_consumer_category_by_tenant_id_string(id_string):
    return ConsumerCategory.objects.filter(tenant__id_string = id_string)

def get_consumer_category_by_id_string(id_string):
    try:
        return ConsumerCategory.objects.get(id_string=id_string)
    except:
        return False


def get_consumer_category_by_id(id):
    try:
        return ConsumerCategory.objects.get(id = id)
    except:
        return False

# End The Code

