import datetime
import uuid
from django.db import models


class CampaignTransaction(models.Model):
    cam_txn_id  = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(Tenant, null=False, blank=False)
    utility = models.ForeignKey(Utility, null=False, blank=False)
    group = models.ForeignKey(CampaignGroup, default=0, null=False, blank=False)
    campaign = models.ForeignKey(CampaignMaster, default=0, null=False, blank=False)
    vendor = models.ForeignKey(VendorDetails, default=0, null=False, blank=False)
    document_type_id = models.IntegerField(default=0, null=False, blank=False)
    document_link = models.IntegerField(default=0, null=False, blank=False)
    status = models.ForeignKey(ScheduleStatus, null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.utcnow())
    updated_date = models.DateField(null=True, blank=True, default=datetime.utcnow())
    created_by = models.ForeignKey(User, null=False, blank=False)
    updated_by = models.ForeignKey(User, null=False, blank=False)

    def __str__(self):
        return self.campaign

    def __unicode__(self):
        return self.campaign