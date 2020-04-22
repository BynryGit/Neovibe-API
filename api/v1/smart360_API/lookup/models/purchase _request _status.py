# table:  Purchase Request Status
# table type: lookup
# table name: 2.12.88 Purchase Request Status (Local)
# table description: It store the purchase request status.
# frequency of data changes: low
# sample table data: "Initiated","Received","Rejected","Pending","Hold"
# reference tables: 2.7.1 Request Master
# auther: Gauri
# creation date: 22/4/2020

#change history
#<ddmmyyyy>-<changes>-<auther>

import datetime  # importing package for datetime
import uuid  # importing package for GUID

from django.db import models  # importing package for database


#Create PurchaseRequestStatus table start
class PurchaseRequestStatus(models.Model):
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

 # Create PurchaseRequestStatus table end