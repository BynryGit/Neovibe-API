# Table Header
# Module: Consumer Care
# Table Type : Master (Global)
# Table Name : 2.4.6. Consumer Token
# Description : All users unique tokens will be saved in this table along with user_id
# Frequency of data changes : High
# Sample table :
# Reference Table : None
# Auther : Jayshree Kumbhare
# Creation Date : 23/04/2020


import datetime
import uuid

from django.db import models

# Create Consumer Token Table Start.

class ConsumerToken(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=False, null=False)
    utility = models.ForeignKey(UtilityMaster, blank=False, null=False)
    consumer_id = models.IntegerField(null=True, blank=True)
    token = models.CharField(null=True, blank=True)
    form_factor_id = models.IntegerField(null=True, blank=True)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.token

    def __unicode__(self):
        return self.token

# Create Consumer Token table end.
