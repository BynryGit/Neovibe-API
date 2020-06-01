# table header
# module: O&M
# table type : Master
# table name : 2.6.2 SOP Master
# table description : This table will store main sop with respect to service type.
# frequency of data changes : High
# sample table data : "Step 1"
# reference tables : None
# author : Jayshree Kumbhare
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.models.service_type import get_service_type_by_id
# Create SOP Master table start

class SopMaster(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    city_id = models.BigIntegerField(null=True, blank=True)
    service_type_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    effective_start_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    effective_end_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.service_type_id) + '-' + str(self.name)

    def __unicode__(self):
        return str(self.service_type_id) + '-' + str(self.name)

    @property
    def get_city(self):
        city_id = get_city_by_id(self.city_id)
        return city_id

    @property
    def get_service_type(self):
        service_type_id = get_service_type_by_id(self.service_type_id)
        return service_type_id


def get_sop_by_id_string(id_string):
    try:
        return SopMaster.objects.get(id_string=id_string)
    except:
        return False

def get_sop_by_id(id):
    try:
        return SopMaster.objects.get(id=id)
    except:
        return False

# Create SOP Master table end.
