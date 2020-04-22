import datetime
import uuid
from django.db import models

# Table Type : Lookup
# Table Name : 2.12.57 Jobcard Status
# Description : It will store the Job Card Status.
# Frequency of data changes : Low
# Reference Table : 2.3.8.3 Jobcard
# Auther : Jayshree
# Creation Date : 21-04-2020


class JobCardStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    job_card_status = models.CharField(max_length=30, blank=False, null=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.job_card_status

    def __unicode__(self):
        return self.job_card_status
