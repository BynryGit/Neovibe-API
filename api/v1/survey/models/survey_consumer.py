# table header
# Module : S&M | Sub-Module : Survey
# table type : Transaction (Local)
# table name : 2.3.4 Survey Consumer Table
# table description : A transaction table to store consumer details for given consumer survey
# frequency of data changes : high
# sample tale data : "Meter No", "Address", "Phone No", "Email"
# Reference Table :
# author : Saloni Monde
# created on : 23/04/2020

# change history
# <ddmmyyyy><changes><author>


import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from v1.supplier.models.supplier import get_supplier_by_id
from v1.survey.models.survey import get_survey_by_id


# Create Survey Consumer table start

class SurveyConsumer(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, null=True, blank=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, null=True, blank=True, on_delete=models.SET_NULL)
    survey_id = models.BigIntegerField(null=False, blank=False)
    vendor_id = models.BigIntegerField(null=False, blank=False)
    consumer_no = models.CharField(max_length=200, null=False, blank=False)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    middle_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    email_id = models.CharField(max_length=200, null=True, blank=True)
    phone_mobile = models.CharField(max_length=200, null=True, blank=True)
    address_line_1 = models.CharField(max_length=500, null=True, blank=True)
    street = models.CharField(max_length=200, null=True, blank=True)
    zipcode = models.BigIntegerField(null=True, blank=True)
    area_id = models.BigIntegerField(null=True, blank=True)
    sub_area_id = models.BigIntegerField(null=True, blank=True)
    category_id = models.BigIntegerField(null=True, blank=True)
    sub_category_id = models.BigIntegerField(null=True, blank=True)
    # field_name = models.CharField(max_length=200, null=False, blank=False)
    # field_type = models.BigIntegerField(null=False, blank=False)
    # field_value = models.CharField(max_length=500, null=False, blank=False)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.first_name

    def __unicode__(self):
        return self.first_name

    @property
    def get_survey(self):
        survey = get_survey_by_id(self.survey_id)
        return survey

    @property
    def get_vendor(self):
        vendor = get_supplier_by_id(self.vendor_id)
        return vendor

def get_survey_consumer_by_id_string(id_string):
    return SurveyConsumer.objects.get(id_string = id_string)

def get_survey_consumer_by_tenant_id_string(id_string):
    return SurveyConsumer.objects.filter(tenant__id_string = id_string)

def get_survey_consumer_by_id(id):
    return SurveyConsumer.objects.get(id = id)



# Create Survey Consumer table end
