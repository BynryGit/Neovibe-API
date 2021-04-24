# table header
# module: billing | sub-module - billing
# table type : lookup (Local)
# table name : Bill Master
# table description : A lookup table for  Bill  of given Bill.
# frequency of data changes : Low
# sample tale data : 
# reference tables : Bill Master Table
# author : Priyanka 
# created on : 01/03/2021

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
import fsm
from django.contrib.postgres.fields import JSONField
import fsm
from django.utils import timezone # importing package for datetime
from v1.commonapp.views.custom_exception import CustomAPIException
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image, ImageDraw

# *********** BILL CONSTANTS **************
BILL_DICT = {
    "CREATED": 0,
    "UN BILLED": 1,
    "IN PROGRESS": 2,
    "PARTIAL": 3,
    "HOLD": 4,
    "COMPLETED": 5,
    "APPROVED": 6,
    "ARCHIVED": 7,
}


# Create Bill Master table start.

class Bill(models.Model, fsm.FiniteStateMachineMixin):

    CHOICES = (
        (0, 'CREATED'),
        (1, 'UN BILLED'),
        (2, 'IN PROGRESS'),
        (3, 'PARTIAL'),
        (4, 'HOLD'),
        (5, 'COMPLETED'),
        (6, 'APPROVED'),
        (7, 'ARCHIVED'),
    )

    state_machine = {
        BILL_DICT['CREATED']: (BILL_DICT['UN BILLED'],),
        BILL_DICT['UN BILLED']: (BILL_DICT['IN PROGRESS'],),
        BILL_DICT['IN PROGRESS']: (BILL_DICT['PARTIAL'],BILL_DICT['COMPLETED'],),
        BILL_DICT['PARTIAL']: (BILL_DICT['COMPLETED'],),
        BILL_DICT['COMPLETED']: (BILL_DICT['APPROVED'],BILL_DICT['HOLD'],),
        BILL_DICT['HOLD']: (BILL_DICT['APPROVED'],),
        BILL_DICT['APPROVED']: (BILL_DICT['ARCHIVED'],),
    }

    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    bill_schedule_log_id = models.BigIntegerField(null=True, blank=True)
    consumer_service_contract_detail_id = models.BigIntegerField(null=True, blank=True)
    bill_cycle_id = models.BigIntegerField(null=True, blank=True)
    consumer_no = models.CharField(max_length=200, null=True, blank=True)
    state = models.BigIntegerField(choices=CHOICES, default=0)
    bill_month = models.CharField(max_length=200, blank=False, null=False)
    bill_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    bill_period = models.CharField(max_length=200, blank=False, null=False)
    meter_reading = JSONField(blank=True, null=True)
    rate_details = JSONField(blank=True, null=True)
    additional_charges = JSONField(blank=True, null=True)
    opening_balance = models.CharField(max_length=200, blank=False, null=False)
    current_charges = models.CharField(max_length=200, blank=False, null=False)
    bill_frequency_id = models.BigIntegerField(null=True, blank=True)
    invoice_no = models.CharField(max_length=200, null=True, blank=True)
    invoice_template = models.TextField(max_length=20000, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    is_adjusted = models.BooleanField(default=False)
    is_spot_bill = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    qr_code = models.FileField(null=True, blank=True)

    
    def __str__(self):
        return str(self.id_string)+"-"+str(self.consumer_service_contract_detail_id)

    def __unicode__(self):
        return self.id_string

    # def save(self, *args, **kwargs):
    #     qrcode_img = qrcode.make(self.link)
    #     canvas = Image.new('RGB', (350, 350), 'white')
    #     canvas.paste(qrcode_img)
    #     fname = f'{self.consumer_no}.png'
    #     buffer = BytesIO()
    #     canvas.save(buffer,'PNG')
    #     self.qr_code.save(fname, File(buffer), save=False)
    #     canvas.close()
    #     super().save(*args, **kwargs)

    
    # Function for finite state machine state change
    def on_change_state(self, previous_state, next_state, **kwargs):
        try:
            self.save()
        except Exception as e:
            raise CustomAPIException("Billing transition failed", status_code=status.HTTP_412_PRECONDITION_FAILED)


# Create Bill Master table end.

def get_bill_by_tenant_id_string(tenant_id_string):
    return Bill.objects.filter(tenant__id_string=tenant_id_string)

def get_bill_by_id_string(id_string):
    try:
        return Bill.objects.get(id_string = id_string)
    except:
        return False

def get_bill_by_id(id):
    try:
        return Bill.objects.get(id = id)
    except:
        return False

def get_bill_by_consumer_service_contract_detail_id(consumer_service_contract_detail_id):
    try:
        return Bill.objects.get(consumer_service_contract_detail_id = id)
    except:
        return False

def get_bill_by_schedule_log_consumer_no(consumer_no,schedule_log_id):
    try:
        return Bill.objects.filter(consumer_no=consumer_no,bill_schedule_log_id=schedule_log_id).last()
    except:
        return False