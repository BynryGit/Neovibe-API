# table header
# module: All  | sub-module - All
# table type : Master
# table name : 2.5.3. User Details
# table description : A master table that stores details of all users in the system.
# frequency of data changes : Low
# sample tale data : "user1", "user2"
# reference tables : 2.5.4 Product/Services Table
# author : Saloni Monde
# created on : 24/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime

from v1.commonapp.models.department import get_department_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.userapp.models.user_role import get_role_by_id
from v1.userapp.models.user_status import get_user_status_by_id
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.contrib.auth.models import User


# Create User Details table start

class UserDetail(User):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    city_id = models.BigIntegerField(blank=True, null=True)
    user_type_id = models.BigIntegerField(null=True, blank=True)  # Tenant, Utility
    user_subtype_id = models.BigIntegerField(null=True, blank=True)  # employee, vendor, supplier
    form_factor_id = models.BigIntegerField(null=True, blank=True)  # Web, Mobile
    user_ID = models.CharField(null=True, blank=True)  # Web, Mobile
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    user_image = models.URLField(null=True, blank=True)
    salt = models.CharField(max_length=200, null=True, blank=True)
    phone_mobile = models.CharField(max_length=200, null=True, blank=True)
    phone_landline = models.CharField(max_length=200, null=True, blank=True)
    department_id = models.BigIntegerField(null=True, blank=True)
    role_id = models.BigIntegerField(null=True, blank=True)
    status_id = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.first_name

    def __unicode__(self):
        return self.first_name

    @property
    def get_user_status(self):
        status = get_user_status_by_id(self.status_id)
        return status.status

    @property
    def get_department(self):
        department = get_department_by_id(self.department_id)
        return department.name

    @property
    def get_user_role(self):
        role = get_role_by_id(self.role_id)
        return role.role

# Create User Details table end


def get_user_by_id_string(id_string):
    return UserDetail.objects.filter(id_string = id_string, is_active=True).last()


def get_user_by_id(id):
    user = UserDetail.objects.filter(id = id, is_active=True).last()
    return user


def get_user_by_username(username):
    return UserDetail.objects.get(username=username)


def get_users_by_tenant_id_string(id_string):
    return UserDetail.objects.filter(tenant__id_string=id_string)