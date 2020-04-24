# table header
# module: Asset
# table type : Master
# table name : 2.6.2.6 Asset Service History
# table description : It will store asset transactions related to service request.
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
import datetime  # importing package for datetime

from django.db import models  # importing package for database
from decimal import Decimal


# Create Asset Service History table start

class AsssetServiceHistory(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    service_request_id = models.IntegerField(null=True, blank=True)
    asset_master_id = models.IntegerField(null=True, blank=True)
    transaction_type = models.IntegerField(null=True, blank=True)
    status_id = models.IntegerField(null=True, blank=True)
    asset_value = models.IntegerField(null=True, blank=True)
    installation_date = models.DateField(null=True, blank=True, default=datetime.now())
    current_value = models.IntegerField(null=True, blank=True)
    life = models.IntegerField(null=True, blank=True)
    maintenance_cost = models.FloatField(max_length=200, blank=False, null=False, default=Decimal(0.00))
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __unicode__(self):
        return self.id

# Create Asset Service History table end.