import datetime
import uuid
from django.db import models

# Create Campain Master table start.
class CampaignMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=False, blank=False)
    utility = models.ForeignKey(UtilityMaster, null=False, blank=False)
    cam_group_id = models.CharField(null=False, blank=False)
    name = models.CharField(null=False, blank=False)
    objective_id = models.IntegerField(default=0,null=False, blank=False)
    description = models.textfield(null=False, blank=False)
    frequency_id = models.IntegerField(default=0, null=False, blank=False)
    type_id = models.IntegerField(default=0, null=False, blank=False)
    potential_consumers = models.IntegerField(default=0, null=False, blank=False)
    actual_consumers = models.IntegerField(default=0, null=False, blank=False)
    budget_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=False, blank=False)
    actual_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0, null=False, blank=False)
    category = models.CharField(null=False, blank=False)
    sub_category = models.CharField(null=False, blank=False)
    start_date = models.DateField(null=True, blank=True, default=datetime.utcnow())
    end_date = models.DateField(null=True, blank=True, default=datetime.utcnow())
    area = models.ForeignKey(Area,default=0, null=False, blank=False)
    sub_area = models.ForeignKey(SubArea,default=0, null=False, blank=False)
    doc_url = models.URLField(max_length=200)
    status = models.ForeignKey(ScheduleStatus, null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.utcnow())
    updated_date = models.DateField(null=True, blank=True, default=datetime.utcnow())
    created_by = models.ForeignKey(User, null=False, blank=False)
    updated_by = models.ForeignKey(User, null=False, blank=False)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name