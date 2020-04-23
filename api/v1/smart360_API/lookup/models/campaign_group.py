# table header
# module: S&M | sub-module - Campaign Group
# table type : lookup (Local)
# table name : 2.12.40 Campaign Group
# table description : A lookup table for campaign groups.
# frequency of data changes : Low
# sample tale data : "campaign_group_1" , "campaign_group_2"
# reference tables : 2.3.6 Campaign Master Table , 2.3.7 Activity Assignment Table , 2.3.8 Campaign Transaction Table
# author : Saloni Monde
# created on : 21/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models   # importing package for database


# Create Campaign Group table start.

class CampaignGroup(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    name = models.CharField(max_length=500, blank=False, null=False)
    status = models.CharField(blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
# Create Campaign Group table end.


def get_camp_type_by_tenant_id_string(tenant_id_string):
    return CampaignGroup.objects.filter(tenant__id_string=tenant_id_string)

def get_camp_type_by_id_string(id_string):
    return CampaignGroup.objects.get(id_string = id_string)
