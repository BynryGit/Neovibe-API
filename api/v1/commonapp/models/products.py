# table header
# module:  
# table type : Master
# table name : Mandatory Fields
# table description :  It will contain details for Product
# frequency of data changes : Low
# sample table data : "Activate", "Deactive"
# reference tables :
# author : Priyanka
# created on : 12/10/2020


from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid  # importing package for GUID

from django.db import models  # importing package for database


# Create Product table start

class Product(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

 # Create Product table end
