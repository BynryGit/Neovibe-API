import uuid
from datetime import datetime
from django.db import models
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.utils import timezone # importing package for datetime

STATE_CONFIGURATION_DICT = {
    "ASSET"           : 0,
    "BILLING"         : 1,
    "CAMPAIGN"        : 2,
    "CONSUMER"        : 3,
    "CONTRACT"        : 4,
    "DISPATCHER"      : 5,
    "EMPLOYEE"        : 6,
    "METER READING"   : 7,
    "PAYMENT"         : 8,
    "PAYROLL"         : 9,
    "REGISTRATION"    : 10,
    "REQUEST"         : 11,
    "SERVICE"         : 12,
    "STORE"           : 13,
    "SUPPLIER"        : 14,
    "SURVEY"          : 15,
    "SYETEM"          : 16,
    "TENANT"          : 17,
    "USER"            : 18,
    "UTILITY"         : 19,
}


class StateConfiguration(models.Model):
    CHOICES = (
        (0, 'ASSET'),
        (1, 'BILLING'),
        (2, 'CAMPAIGN'),
        (3, 'CONSUMER'),
        (4, 'CONTRACT'),
        (5, 'DISPATCHER'),
        (6, 'EMPLOYEE'),
        (7, 'METER READING'),
        (8, 'PAYMENT'),
        (9, 'PAYROLL'),
        (10, 'REGISTRATION'),
        (11, 'REQUEST'),
        (12, 'SERVICE'),
        (13, 'STORE'),
        (14, 'SUPPLIER'),
        (15, 'SURVEY'),
        (16, 'SYETEM'),
        (17, 'TENANT'),
        (18, 'USER'),
        (19, 'UTILITY'),
    )
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    sender_object = models.BigIntegerField(choices=CHOICES, default=0)
    sender_state = models.BigIntegerField(null=True, blank=True)
    receiver_object = models.BigIntegerField(choices=CHOICES, default=0)
    receiver_state = models.BigIntegerField(null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.utility.name

    def __unicode__(self):
        return self.utility.name