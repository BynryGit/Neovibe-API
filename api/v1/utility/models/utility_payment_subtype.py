import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime

from v1.payment.models.payment_sub_type import get_payment_sub_type_by_id
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from v1.commonapp.views.custom_exception import CustomAPIException
from rest_framework import status
from v1.utility.models.utility_payment_type import get_utility_payment_type_by_id
from django.utils import timezone # importing package for datetime


# Create Utility Payment table start


class UtilityPaymentSubtype(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    payment_subtype_id = models.BigIntegerField(null=True, blank=True)
    payment_type_id = models.BigIntegerField(null=True, blank=True)
    name = models.CharField(max_length=200, blank=False, null=False)
    gl_code = models.CharField(max_length=200, blank=True, null=True)
    tax = models.DecimalField(blank=True, null=True, max_digits=10, decimal_places=4)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.name + ' ' + str(self.id_string)

    def __unicode__(self):
        return self.name

    @property
    def get_payment_type(self):
        payment_type = get_utility_payment_type_by_id(self.payment_type_id)
        print(payment_type)
        return payment_type

    @property
    def get_payment_sub_type_key(self):
        payment_sub_type = get_payment_sub_type_by_id(self.payment_subtype_id)
        return payment_sub_type.key


def get_utility_payment_subtype_by_id(id):
    try:
        return UtilityPaymentSubtype.objects.filter(id=id)
    except Exception as e:
        raise CustomAPIException("Utility Payment Subtype does not exists.", status_code=status.HTTP_404_NOT_FOUND)


def get_utility_payment_subtype_by_id_string(id_string):
    try:
        return UtilityPaymentSubtype.objects.get(id_string=id_string)
    except:
        return False
# Create Utility Payment table end.
