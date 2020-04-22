# table: Store Location
# table type: lookup
# table name: 2.12.91 Store Location (Local)
# table description: It store the Store Location .
# frequency of data changes: Medium
# sample table data:
# reference tables: 2.7.10 Store Master
# auther: Gauri
# creation date: 22/4/2020

#change history
#<ddmmyyyy>-<changes>-<auther>

import datetime  # importing package for datetime
import uuid  # importing package for GUID

from django.db import models  # importing package for database


#Create StoreLocation table start
class StoreLocation(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=False, blank=False)
    utility = models.ForeignKey(UtilityMaster, null=False, blank=False)
    store_location = models.CharField(null=False, blank=False)
    city_id = models.CharField(null=False, blank=False)
    created_by = models.CharField(null=False, blank=False)
    updated_by = models.CharField(null=False, blank=False)
    created_date = models.DateTime(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTime(null=True, blank=True, default=datetime.now())
    is_active = models.Boolean(default=False)

    def __str__(self):
        return self.store_location

    def __unicode__(self):
        return self.store_location

 # Create StoreLocation table end