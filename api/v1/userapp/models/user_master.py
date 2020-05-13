import uuid  # importing package for guid
import jsonfield # importing json field
from datetime import datetime # importing package for datetime

from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.models.department import get_department_by_id
from v1.commonapp.models.document import get_documents_by_user_id
from v1.commonapp.models.form_factor import get_form_factor_by_id
from v1.commonapp.models.notes import get_notes_by_user_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.userapp.models.user_bank_detail import get_bank_by_id
from v1.userapp.models.user_role import get_role_by_id
from v1.userapp.models.user_status import get_user_status_by_id
from v1.userapp.models.user_sub_type import get_user_sub_type_by_id
from v1.userapp.models.user_type import get_user_type_by_id
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from django.contrib.auth.models import User

# Create User Details table start

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


class UserDetail(User):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    city_id = models.BigIntegerField(blank=True, null=True)
    user_type_id = models.BigIntegerField(null=True, blank=True)  # Tenant, Utility
    user_subtype_id = models.BigIntegerField(null=True, blank=True)  # employee, vendor, supplier
    form_factor_id = models.BigIntegerField(null=True, blank=True)  # Web, Mobile
    user_ID = models.CharField(max_length=200,null=True, blank=True)  # Web, Mobile
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    user_image = models.URLField(null=True, blank=True)
    salt = models.CharField(max_length=200, null=True, blank=True)
    phone_mobile = models.CharField(max_length=200, null=True, blank=True)
    phone_landline = models.CharField(max_length=200, null=True, blank=True)
    department_id = models.BigIntegerField(null=True, blank=True)
    status_id = models.BigIntegerField(null=True, blank=True)
    utilities = jsonfield.JSONField()
    skills = jsonfield.JSONField()
    areas = jsonfield.JSONField()
    bank_detail_id = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __unicode__(self):
        return self.id

    @property
    def get_tenant(self):
        return self.tenant

    @property
    def get_utility(self):
        return self.utility

    @property
    def get_user_status(self):
        return get_user_status_by_id(self.status_id)

    @property
    def get_city(self):
        return get_city_by_id(self.city_id)

    @property
    def get_type(self):
        return get_user_type_by_id(self.user_type_id)

    @property
    def get_sub_type(self):
        return get_user_sub_type_by_id(self.user_subtype_id)

    @property
    def get_department(self):
        return get_department_by_id(self.department_id)

    @property
    def get_form_factor(self):
        return get_form_factor_by_id(self.form_factor_id)

    @property
    def get_user_role(self):
        return get_role_by_id(self.role_id)

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


def get_bank_by_user_id_string(id_string):
    user = UserDetail.objects.filter(id_string=id_string).last()
    return get_bank_by_id(user.bank_detail_id)


def get_documents_by_user_id_string(id_string):
    user = UserDetail.objects.filter(id_string=id_string, is_active=True).last()
    return get_documents_by_user_id(user.id)


def get_notes_by_user_id_string(id_string):
    user = UserDetail.objects.filter(id_string=id_string, is_active=True).last()
    return get_notes_by_user_id(user.id)