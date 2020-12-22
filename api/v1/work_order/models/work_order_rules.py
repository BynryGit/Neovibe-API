# table header
# module: Work Order | sub-module -
# Table Type : Lookup (Global)
# Table Name : WorkOrderRule
# Description : It is a global lookup table that stores areas within Rules.
# Frequency of data changes : Low
# Sample table :
# Reference Table :WorkOrderRule
# Author : Priyanka 
# Creation Date : 21/12/2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from django.db import models  # importing package for database

from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.views.custom_exception import ObjectNotFoundException
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.commonapp.models.region import get_region_by_id
from v1.commonapp.models.country import get_country_by_id
from v1.commonapp.models.state import get_state_by_id
from v1.commonapp.models.city import get_city_by_id


# Create WorkOrderRule table start


class WorkOrderRule(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    rule_id = models.BigIntegerField(null=True, blank=True)
    rule = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.rule 

    def __unicode__(self):
        return self.rule

    @property
    def get_tenant(self):
        return self.tenant

    @property
    def get_utility(self):
        return self.utility


# Create WorkOrderRule table end

def get_work_order_rule_by_tenant_id_string(id_string):
    return WorkOrderRule.objects.filter(tenant__id_string=id_string)


def get_work_order_rule_by_utility_id_string(id_string):
    return WorkOrderRule.objects.filter(utility__id_string=id_string)


def get_work_order_rule_by_id(id):
    try:
        return WorkOrderRule.objects.get(id=id)
    except:
        return False


def get_work_order_rule_by_id_string(id_string):
    try:
        return WorkOrderRule.objects.get(id_string=id_string)
    except:
        return False
