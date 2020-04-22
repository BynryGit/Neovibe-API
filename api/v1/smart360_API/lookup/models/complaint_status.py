# table: Complaint Status
# table type: lookup
# table name: 2.12.49 Complaint Status (Local)
# table description: The complaint status store in this table with respect to the complaint.
# frequency of data changes: low
# sample table data: "Received","Complete","Rejected","Pending","Hold"
# reference tables: 2.3.5. Consumer - complaints
# auther: Gauri
# creation date: 22/4/2020

#change history
#<ddmmyyyy>-<changes>-<auther>

import datetime  # importing package for datetime
import uuid  # importing package for GUID

from django.db import models  # importing package for database


#Create ComplaintStatus table start
class ComplaintStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=False, blank=False)
    utility = models.ForeignKey(UtilityMaster, null=False, blank=False)
    status = models.CharField(null=False, blank=False)
    created_by = models.CharField(null=False, blank=False)
    updated_by = models.CharField(null=False, blank=False)
    created_date = models.DateTime(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTime(null=True, blank=True, default=datetime.now())
    is_active = models.Boolean(default=False)

    def __str__(self):
        return self.status

    def __unicode__(self):
        return self.status

 # Create ComplaintStatus table end