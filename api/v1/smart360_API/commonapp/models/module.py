# table header
# module: All | sub-module - All
# table type : lookup (Local)
# table name : 2.12.42 Campaign Transaction Status
# table description : A lookup table for all transactions of given campaign.
# frequency of data changes : Low
# sample tale data : "created", "assigned", "started","completed","hold","cancel"
# reference tables : 2.3.6 Campaign Master Table
# author : Saloni Monde
# created on : 21/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database
from api.v1.smart360_API.tenant.models.tenant_master import TenantMaster
from api.v1.smart360_API.utility.models.utility_master import UtilityMaster

# Create Module table start


class Module(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    name = models.CharField(max_length=200, blank=False, null=False)
    created_by = models.IntegerField(blank=False, null=False)
    updated_by = models.IntegerField(blank=False, null=False)
    created_date = models.DateField(default=datetime.now)
    updated_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

# Create Module table start

