# table: Store Type
# table type: lookup
# table name: 2.12.90 Store Type (Local)
# table description: It store the Store Type.
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


#Create StoreType table start
class StoreType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=False, blank=False)
    utility = models.ForeignKey(UtilityMaster, null=False, blank=False)
    type = models.CharField(null=False, blank=False)
    name = models.CharField(null=False, blank=False)
    type_status = models.CharField(null=False, blank=False)
    created_by = models.CharField(null=False, blank=False)
    updated_by = models.CharField(null=False, blank=False)
    created_date = models.DateTime(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTime(null=True, blank=True, default=datetime.now())
    is_active = models.Boolean(default=False)

    def __str__(self):
        return self.type

    def __unicode__(self):
        return self.type

 # Create StoreType table end