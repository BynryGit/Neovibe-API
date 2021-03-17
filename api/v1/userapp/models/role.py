
# module: All  | sub-module - All
# table type :
# table name :
# table description : Skills of a particular user will be stored in this table
# frequency of data changes :
# sample tale data :
# reference tables :
# author : Saloni Monde
# created on : 25/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime

from v1.commonapp.models.department import get_department_by_id
from v1.commonapp.models.form_factor import get_form_factor_by_id
from v1.tenant.models.tenant_master import TenantMaster, get_tenant_by_id
from v1.userapp.models.role_status import get_role_status_by_id
from v1.userapp.models.role_sub_type import get_role_sub_type_by_id, get_role_sub_type_by_id_string
from v1.userapp.models.role_type import get_role_type_by_id, get_role_type_by_id_string
from v1.utility.models.utility_master import UtilityMaster, get_utility_by_id
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime


# Create User Role table start

class Role(models.Model): # change name to role
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    type_id = models.BigIntegerField(blank=True, null=True)
    sub_type_id = models.BigIntegerField(blank=True, null=True)
    form_factor_id = models.BigIntegerField(blank=True, null=True)
    department_id = models.BigIntegerField(blank=True, null=True)
    role_ID = models.CharField(max_length=200,blank=True, null=True)
    role = models.CharField(max_length=200,blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.role

    def __unicode__(self):
        return self.role

    @property
    def get_tenant(self):
        return get_tenant_by_id(self.tenant_id)

    @property
    def get_utility(self):
        return get_utility_by_id(self.utility_id)

    @property
    def get_role_type(self):
        return get_role_type_by_id(self.type_id)

    @property
    def get_role_sub_type(self):
        return get_role_sub_type_by_id(self.sub_type_id)

    @property
    def get_user_status(self):
        return get_role_status_by_id(self.status_id)

    @property
    def get_form_factor(self):
        return get_form_factor_by_id(self.form_factor_id)

    @property
    def get_department(self):
        return get_department_by_id(self.department_id)

    # class Meta:
    #     unique_together = ('type_id', 'sub_type_id', 'form_factor_id', 'department_id', 'role',)


# Create User Role table end


# For getting all roles in table
def get_all_role():
    return Role.objects.filter(is_active=True)


# For getting role by id
def get_role_by_id(id):
    return Role.objects.filter(id=id, is_active=True).last()


# For getting role by id_string
def get_role_by_id_string(id_string):
    try:
        return Role.objects.get(id_string=id_string, is_active=True)
    except:
        return False


# For getting role by tenant id_string
def get_role_by_tenant_id_string(id_string):
    return Role.objects.filter(tenant__id_string=id_string, is_active=True)


# For getting role by utility id_string
def get_role_by_utility_id_string(id_string):
    return Role.objects.filter(utility__id_string=id_string, is_active=True)


# For getting role by type and sub-type id_string
def get_role_by_type_and_sub_type(type_id_string, sub_type_id_string):
    type = get_role_type_by_id_string(type_id_string)
    sub_type = get_role_sub_type_by_id_string(sub_type_id_string)
    return Role.objects.filter(type_id=type.id, sub_type_id=sub_type.id, is_active=True)