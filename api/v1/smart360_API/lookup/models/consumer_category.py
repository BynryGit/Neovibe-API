# Table Header
# module: S&M, Consumer Care & Ops | sub-module - Consumer, Metering, Billing, Payments, Services, Complaints
# Table Type: Lookup (Global)
# Table Name : 2.12.14 Consumer Category
# Description : Lookup table for all consumer categories to be used by Operator or Utility.
# Frequency of data changes : Low
# Sample Table Data : Domestic
# Reference Table : 2.2.2 Service Plans, 2.3.1 Survey Table, 2.3.8 Campaign Transaction Table,
#                    2.3.1. Consumer Master, 2.3.2. Consumer - Registration, 2.4.3 Asset Master, 2.7.1. Employee.
# Auther : Jayshree
# Creation Date : 21/04/2020

import datetime
import uuid
from django.db import models

# Start the Code
class ConsumerCategory(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    category_name = models.CharField(max_length=40, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.category_name

    def __unicode__(self):
        return self.category_name


def get_consumer_category_by_id_string(id_string):
    return ConsumerCategory.objects.get(id_string = id_string)

# End The Code