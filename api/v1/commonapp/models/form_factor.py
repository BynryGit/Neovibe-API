# Table Header
# module: Consumer Care & Ops | sub-module - Consumer, Registration, Billing, Payments, Services, Complaints
# Table Type : Lookup (Global)
# Table Name : 2.12.18 Form Factor
# Description : It is a global lookup table that stores form factors
# Sample Table Data : "Web", "Mobile"
# Frequency of data changes : Low
# Reference Table : 2.4.6. Consumer Token
# Author : Jayshree Kumbhare
# Creation Date : 21-04-2020

# change history
# <ddmmyyyy><changes><author>

import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database

# Create Form Factor table start


class FormFactor(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    @property
    def get_tenant(self):
        return self.tenant

    @property
    def get_utility(self):
        return self.utility

# Create Form Factor table end


def get_all_form_factors():
    return FormFactor.objects.filter(is_active=True)


def get_form_factor_by_tenant_id_string(id_string):
    return FormFactor.objects.filter(tenant__id_string=id_string)


def get_form_factor_by_id_string(id_string):
    return FormFactor.objects.filter(id_string=id_string)


def get_form_factor_by_id(id):
    return FormFactor.objects.filter(id=id)
