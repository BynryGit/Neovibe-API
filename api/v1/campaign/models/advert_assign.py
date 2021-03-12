# table header
# module: S&M | sub-module - Campaign
# table type : Transaction (Local)
# table name : 2.3.6 advertisement assignment
# table description : A transaction table to store vendor assignment for given advertisement
# frequency of data changes : high
# sample tale data : Ads = "Smart360-Awareness" , Vendor = "Bynry"
# author : Priyanka Kachare
# created on : 21/04/2020

# change history
# <ddmmyyyy><changes><author>


from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid
from django.db import models
from django.utils import timezone # importing package for datetime

# Create advertisement assignment table starts

class AdvertisementAssignment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=True, blank=True,on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, null=True, blank=True,on_delete=models.SET_NULL)
    campaign_id = models.BigIntegerField(default=1, null=True, blank=True)
    group_id = models.BigIntegerField(default=1, null=True, blank=True)
    vendor_id = models.BigIntegerField(default=1, null=True, blank=True)  # todo: check actual name
    assigned_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    completion_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    status_id = models.BigIntegerField(default=1, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.vendor_id

    def __unicode__(self):
        return self.vendor_id

    # Create advertisement assignment table ends
