import datetime
import uuid
from django.db import models

# Assign Campain to vendor
class CampaignAssignment(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=False, blank=False)
    utility = models.ForeignKey(Utility, null=False, blank=False)
    group_id = models.IntegerField(default=0, null=False, blank=False)
    campaign = models.ForeignKey(CampaignMaster,default=0, null=False, blank=False)
    vendor = models.ForeignKey(VendorDetails,default=0, null=False, blank=False)
    assigned_date = models.DateField(null=True, blank=True, default=datetime.utcnow())
    completion_date = models.DateField(null=True, blank=True, default=datetime.utcnow())
    status = models.ForeignKey(ScheduleStatus, null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.utcnow())
    updated_date = models.DateField(null=True, blank=True, default=datetime.utcnow())
    created_by = models.ForeignKey(User, null=False, blank=False)
    updated_by = models.ForeignKey(User, null=False, blank=False)

    def __str__(self):
        return self.vendor

    def __unicode__(self):
        return self.vendor