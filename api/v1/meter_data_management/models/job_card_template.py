__author__ = "chinmay"

# Table Header
# Module: Consumer Care & Ops | Sub-Module : Meter Reading, billing, Bill Distribution
# Table Type : Master
# Table Name : JobCardTemplate
# Description : It is JobCardTemplate table. This table will save all the Configuration details of smart meter.
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Author : Chinmay Pathak
# Creation Date : 25/02/2021


import uuid  # importing package for GUID
from django.db import models  # importing package for database
from django.utils import timezone # importing package for datetime
from django.contrib.postgres.fields import JSONField
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.utility.models.utility_product import get_utility_product_by_id


# Create JobCardTemplate Table Start

class JobCardTemplate(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    task_name = models.CharField(max_length=200, blank=True, null=True)
    meter_read_json_obj = JSONField()
    additional_parameter_json = JSONField()
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True, default=timezone.now)

    def __str__(self):
        return self.task_name

    def __unicode__(self):
        return self.task_name



# Create JobCardTemplate Table end


def get_job_card_template_by_id(id):
    try:
        return JobCardTemplate.objects.get(id=id, is_active=True)
    except:
        return False


def get_job_card_template_by_id_string(id_string):
    try:
        return JobCardTemplate.objects.get(id_string=id_string, is_active=True)
    except:
        return False