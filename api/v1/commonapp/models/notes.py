# table header
# module: Sourcing
# table type : Master
# table name : 2.5.12 Notes
# table description : The Notes table saves the Common Notes
# frequency of data changes : High
# sample table data :
# reference tables : None
# author : Jayshree Kumbhare
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime

from v1.commonapp.models.module import get_module_by_id
from v1.commonapp.models.service_type import get_service_type_by_id
from v1.commonapp.models.sub_module import get_sub_module_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.userapp.models.user_master import get_user_by_id
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
# Create Notes Table start

class Notes(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    module_id = models.BigIntegerField(null=True, blank=True)
    sub_module_id = models.BigIntegerField(null=True, blank=True)
    service_type_id = models.BigIntegerField(null=True, blank=True)
    identification_id = models.BigIntegerField(null=True, blank=True)
    note_name = models.CharField(max_length=200, blank=True, null=True)
    note_color = models.BigIntegerField(null=True, blank=True)
    note = models.CharField(max_length=500, blank=True, null=True)
    status = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.note_name

    def __unicode__(self):
        return self.note_name

    @property
    def get_tenant(self):
        return self.tenant

    @property
    def get_utility(self):
        return self.utility

    @property
    def get_module(self):
        return get_module_by_id(self.module_id)

    @property
    def get_sub_module(self):
        return get_sub_module_by_id(self.sub_module_id)

    @property
    def get_service_type(self):
        return get_service_type_by_id(self.service_type_id)

    @property
    def get_user_identification(self):
        return get_user_by_id(self.identification_id)

# Create Notes table end.


def get_notes_by_user_id(id):
    return Notes.objects.filter(identification=id)
