import uuid
from datetime import datetime
from django.db import models
from v1.tenant.models.tenant_master import TenantMaster
# from v1.utility.models.utility_master import UtilityMaster
from django.utils import timezone # importing package for datetime

TRANSITION_CONFIGURATION_DICT = {
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
TRANSITION_CHANNEL_DICT = {
    "EMAIL"           : 0,
    "SMS"             : 1,
    "WHATSAPP"        : 2,
}
class TransitionConfiguration(models.Model):
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
    CHANNEL_CHOICES = (
        (0, 'EMAIL'),
        (1, 'SMS'),
        (2, 'WHATSAPP'),
    )
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey('utility.UtilityMaster', blank=True, null=True, on_delete=models.SET_NULL)
    transition_object = models.BigIntegerField(choices=CHOICES, default=0)
    transition_state = models.BigIntegerField(null=True, blank=True)
    channel = models.BigIntegerField(choices=CHANNEL_CHOICES, default=0)
    event = models.CharField(max_length=200, null=True, blank=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    template_id = models.BigIntegerField(null=True, blank=True)

    def __str__(self):
        return self.tenant.name

    def __unicode__(self):
        return self.tenant.name

def get_transition_configuration_by_id(id):
    try:
        return TransitionConfiguration.objects.get(id = id)
    except Exception as e:
        return False

def is_transition_configuration_exists(transition_object, next_state, utility):
    try:
        fill = TransitionConfiguration.objects.filter(transition_object=transition_object, transition_state=next_state,
                                                  utility=utility, is_active=True).exists()
        print("HHHHHHHHHHHHHHH",transition_object,next_state,utility)
        return fill

    except Exception as e:
        return False