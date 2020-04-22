# table: Route Details
# table type: lookup
# table name: 2.12.50 Route Details (Local)
# table description: It is lookup tables to be used in tables.
# frequency of data changes: Medium
# sample table data:
# reference tables: 2.3.8.2 Reading Consumer Master, 2.3.8.3 Jobcard, 2.3.8.4 Meter Reading, 2.3.9 Invoice/Bill
# auther: Gauri
# creation date: 22/4/2020

#change history
#<ddmmyyyy>-<changes>-<auther>

import datetime  # importing package for datetime
import uuid  # importing package for GUID

from django.db import models  # importing package for database


#Create RouteDetails table start
class RouteDetails(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=False, blank=False)
    utility = models.ForeignKey(UtilityMaster, null=False, blank=False)
    route_code = models.CharField(null=False, blank=False)
    bill_month = models.IntegerField(null=False, blank=False)
    bill_cycle = models.CharField(null=False, blank=False)
    bill_status = models.CharField(null=False, blank=False)
    mru_master = models.CharField(null=False, blank=False)
    created_by = models.CharField(null=False, blank=False)
    updated_by = models.CharField(null=False, blank=False)
    created_date = models.DateTime(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTime(null=True, blank=True, default=datetime.now())
    is_active = models.Boolean(default=False)

    def __str__(self):
        return self.status

    def __unicode__(self):
        return self.status

 # Create RouteDetails table end