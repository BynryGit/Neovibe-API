import datetime  # importing package for datetime
import uuid  # importing package for GUID

from django.db import models  # importing package for database


# table header : RegistrationType
# table type: lookup
# table name: 2.12.46 Registration Type (Local)
# table description: It is a lookup table that stores the various types of registrations to be used in various tables.
# Registration type and ID of Registration type to be used by Operator or Utility
# frequency of data changes: low
# sample table data:
# reference tables: 2.3.2. Consumer - Registration
# auther: Gauri
# creation date: 22/4/2020

# change history

class Registration_Type(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=False, blank=False)
    utility = models.ForeignKey(UtilityMaster, null=False, blank=False)
    registration_type = models.CharField(null=False, blank=False)
    created_by = models.CharField(null=False, blank=False)
    updated_by = models.CharField(null=False, blank=False)
    created_date = models.DateTime(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTime(null=True, blank=True, default=datetime.now())
    is_active = models.Boolean(default=False)

    def __str__(self):
        return self.registration_type

    def __unicode__(self):
        return self.registration_type