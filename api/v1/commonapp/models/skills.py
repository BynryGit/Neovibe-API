# Table Header
# Table Type : Lookup (Local)
# Table Name : 2.12.76 Skills
# Description : It will store the skills of each service type.
# Frequency of data changes : Low
# Sample Table Data :
# Reference Table : 2.6.1 Service Request
# Author : Jayshree Kumbhare
# Creation Date : 22/04/2020

# change history
# <ddmmyyyy>-<changes>-<Author>

from datetime import datetime # importing package for datetime

from v1.commonapp.models.service_type import get_service_type_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID
from django.db import models  # importing package for database


# Create Skills table start

class Skills(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    skill = models.CharField(max_length=200, blank=False, null=False)
    description = models.CharField(max_length=500, blank=False, null=False)
    service_type_id = models.BigIntegerField(blank=False, null=False)
    created_by = models.BigIntegerField(null=False, blank=False)
    updated_by = models.BigIntegerField(null=False, blank=False)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.skill

    def __unicode__(self):
        return self.skill

    @property
    def get_tenant(self):
        return self.tenant

    @property
    def get_utility(self):
        return self.utility

    @property
    def get_service_type(self):
        return get_service_type_by_id(self.service_type_id)

# Create Skills table end


def get_skills_by_utility_id_string(id_string):
    return Skills.objects.filter(utility__id_string=id_string)