# table header
# module: S&M  | sub-module - Survey,campaign
# table type : lookup (Local)
# table name : 2.12.34 Survey Transaction Status
# table description : A lookup table for all transaction status for given survey campaign.
# frequency of data changes : Low
# sample tale data : "created", "assigned", "started","completed","hold","cancel"
# reference tables : 2.3.3 Survey Transaction Table
# author : Saloni Monde
# created on : 21/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database


# Create Survey Transaction Status table start.

class SurveyTransactionStatus(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=True, blank=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, null=True, blank=True, on_delete=models.SET_NULL)
    status = models.CharField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.status

    def __unicode__(self):
        return self.status

def get_survey_transaction_status_by_id_string(id_string):
    return SurveyTransactionStatus.objects.filter(tenant__id_string = id_string)

def get_survey_transaction_status_by_tenant_id_string(id_string):
    return SurveyTransactionStatus.objects.get(id_string = id_string)

def get_survey_transaction_status_by_id(id):
    return SurveyTransactionStatus.objects.get(id = id)

# Create Survey Transaction Status table end.
