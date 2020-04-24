#table header
# module: Consumer Care & Ops | sub-module - Consumer, Metering & Billing
#table type: lookup
#table name: 2.12.44 Portion  (Local)
#table description: It portion and ID of various portion to be used by Operator or Utility
# #frequency of data changes: low
#sample table data:
#reference tables: 2.3.1. Consumer Master
#auther: Gauri
#creation date: 21/4/2020

#change history
#<ddmmyyyy>-<changes>-<auther>

import datetime #importing package for datetime
import uuid #importing package for GUID

from django.db import models #importing package for database


#Create Portion table start
class Portion(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True) #TODO: remove _id: Done
    tenant = models.ForeignKey(TenantMaster,null=False, blank=False)  #Table name : Done
    utility = models.ForeignKey(UtilityMaster,null=False, blank=False)  # Table name:Done
    portion_name = models.CharField(null=False, blank=False)#TODO: Name: Done
    city_id = models.CharField(null=False, blank=False) #TODO: remove foreignkey :Done
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())


    def __str__(self):
        return self.portion_name

    def __unicode__(self):
        return self.portion_name
    # Create Portion table end