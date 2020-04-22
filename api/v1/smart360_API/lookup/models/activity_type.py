import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database


# table header
# table type : lookup
# table name : 2.12.43 Activity Type
# table description : It is a lookup table for activity type to be used in tables
# frequency of data changes : Medium
# sample tale data :
# reference tables : TenantMaster, UtilityMaster
# auther : Saloni

# change history
# 21/04/2020 Creation Saloni

class ActivityType(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    activity_type_name = models.CharField(max_length=200, blank=False, null=False)
    created_by = models.CharField(blank=False, null=False)
    updated_by = models.CharField(blank=False, null=False)
    created_date = models.DateField(default=datetime.now)
    updated_date = models.DateField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.activity_type_name