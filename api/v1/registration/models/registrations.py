from django.contrib.postgres.fields import JSONField

from v1.commonapp.models.area import get_area_by_id
from v1.commonapp.models.transition_configuration import TRANSITION_CONFIGURATION_DICT
from v1.consumer.models.consumer_category import *
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id
from v1.registration.views.common_functions import *
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
import uuid
from django.db import models
import fsm
from v1.commonapp.views.custom_exception import CustomAPIException
from django.contrib.postgres.fields import JSONField
from django.utils import timezone # importing package for datetime
from v1.commonapp.models.state import get_state_by_id

# *********** REGISTRATION CONSTANTS **************
REGISTRATION_DICT = {
    "CREATED": 0,
    "APPROVED": 1,
    "REJECTED": 2,
    "HOLD": 3,
}


# table header
# module: S&M,Consumer care and ops | sub-module - Registration
# table type : Master
# table name : 2.4.2 Registration Master
# table description : A master table to store new registration details.
# frequency of data changes : High
# sample table data : "Registration 1" , "Registration 2" , "Registration 3"
# reference tables : None
# author : Rohan Wagh
# created on : 21/04/2020

# Create Consumer Registration table start.
class Registration(models.Model, fsm.FiniteStateMachineMixin):
    CHOICES = (
        (0, 'CREATED'),
        (1, 'APPROVED'),
        (2, 'REJECTED'),
        (3, 'HOLD'),       
    )

    state_machine = {
        REGISTRATION_DICT['CREATED']: (REGISTRATION_DICT['APPROVED'], REGISTRATION_DICT['CREATED'], REGISTRATION_DICT['REJECTED'], REGISTRATION_DICT['HOLD']),
        REGISTRATION_DICT['HOLD']: (REGISTRATION_DICT['APPROVED'], REGISTRATION_DICT['REJECTED']),
    }

    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    state = models.BigIntegerField(choices=CHOICES, default=0)
    registration_no = models.CharField(max_length=200, null=True, blank=True)
    email_id = models.CharField(max_length=200, null=True, blank=True)
    phone_mobile = models.CharField(max_length=200, null=True, blank=True)
    phone_landline = models.CharField(max_length=200, null=True, blank=True)
    billing_address_line_1 = models.CharField(max_length=200, blank=True, null=True)
    billing_street = models.CharField(max_length=200, blank=True, null=True)
    billing_zipcode = models.CharField(max_length=200, null=True, blank=True)
    billing_state_id = models.BigIntegerField(null=True, blank=True)
    billing_city_id = models.BigIntegerField(null=True, blank=True)
    billing_area_id = models.BigIntegerField(null=True, blank=True)
    billing_sub_area_id = models.BigIntegerField(null=True, blank=True)
    premise_id = models.BigIntegerField(null=True, blank=True)
    credit_rating_id = models.BigIntegerField(null=True, blank=True)
    registration_obj = JSONField(null=True, blank=True)
    is_auto_pay = models.BooleanField(default=False)
    is_loan = models.BooleanField(default=False)
    is_upfront_amount = models.BooleanField(default=False)
    ownership_id = models.BigIntegerField(null=True, blank=True)
    is_address_same = models.BooleanField(default=False)
    is_vip = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.email_id + " " + str(self.id_string)

    def __unicode__(self):
        return self.email_id

    # @property
    # def get_area(self):
    #     area = get_area_by_id(self.area_id)
    #     return area
    
    @property
    def get_area(self):
        area = get_area_by_id(self.billing_area_id)
        return {
            'name': area.name,
            'id_string': area.id_string
        }

    @property
    def get_state(self):
        state = get_state_by_id(self.billing_state_id)
        return {
            'name': state.name,
            'id_string': state.id_string
        }

    @property
    def get_consumer_category(self):
        category = get_consumer_category_by_id(self.consumer_category_id)
        return category

    @property
    def get_consumer_sub_category(self):
        sub_category = get_consumer_sub_category_by_id(self.sub_category_id)
        return sub_category

    def on_change_state(self, previous_state, next_state, **kwargs):
        try:
            perform_events(next_state, self, TRANSITION_CONFIGURATION_DICT["REGISTRATION"])
            perform_signals(next_state, self)
            self.save()
        except Exception as e:
            raise CustomAPIException("Registration transition failed", status_code=status.HTTP_412_PRECONDITION_FAILED)


def get_registration_by_id_string(id_string):
    try:
        return Registration.objects.get(id_string=id_string)
    except:
        return False


def get_registration_by_id(id):
    try:
        return Registration.objects.get(id=id)
    except:
        return False


def get_registration_by_registration_no(no):
    try:
        return Registration.objects.get(registration_no = no)
    except:
        return False
# Create Consumer Registration table end.
