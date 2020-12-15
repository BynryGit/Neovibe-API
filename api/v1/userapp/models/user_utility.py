# table header
# module: All  | sub-module - All
# table type :
# table name :
# table description : A master table that stores user wise privileges.
# frequency of data changes : Low
# sample tale data :
# reference tables :
# author : Saloni Monde
# created on : 25/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime

from v1.tenant.models.tenant_master import TenantMaster, get_tenant_by_id
from v1.utility.models.utility_master import UtilityMaster, get_utility_by_id, get_utility_by_id_string
from django.db import models  # importing package for database


# Create User Privilege table start

class UserUtility(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    user_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    # def __str__(self):
    #     return self.tenant.name

    def __unicode__(self):
        return self.user_id

    @property
    def get_tenant(self):
        return get_tenant_by_id(self.tenant.id)

    @property
    def get_utility(self):
        return get_utility_by_id(self.utility.id)
    #
    # @property
    # def get_user(self):
    #     return get_user_by_id(self.user_id)


# Create User Privilege table end

def check_user_utility_exists(user_id, utility_id):
    return UserUtility.objects.filter(user_id=user_id, utility_id=utility_id, is_active=True).exists()


def get_utility_by_user(user_id):
    return UserUtility.objects.filter(user_id=user_id, is_active=True)


def get_record_by_values(user_id_string, utility_id_string):
    user = get_user_by_id_string(user_id_string)
    utility = get_utility_by_id_string(utility_id_string)
    return UserUtility.objects.filter(user_id=user.id,utility=utility).last()

