import uuid  # importing package for guid
from datetime import datetime # importing package for datetime

from django.db import models  # importing package for database

# Create Consumer Support table start
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.consumer.models.consumer_category import get_consumer_category_by_id
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id
from v1.commonapp.models.city import get_city_by_id


class ConsumerSupport(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    category_id = models.BigIntegerField(blank=True, null=True)
    subcategory_id = models.BigIntegerField(blank=True, null=True)
    city_id = models.BigIntegerField(blank=True,null=True)
    email_id = models.CharField(max_length=200, blank=True, null=True)
    phone_no = models.CharField(max_length=200, blank=True, null=True)
    description = models.CharField(max_length=200, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
    
    @property
    def get_category_type(self):
        consumer_category = get_consumer_category_by_id(self.category_id)
        return consumer_category
    
    @property
    def get_category_subtype(self):
        consumer_subcategory = get_consumer_sub_category_by_id(self.subcategory_id)
        return consumer_subcategory
    
    @property
    def get_city(self):
        city = get_city_by_id(self.city_id)
        return city

# Create Consumer Support table end

def get_consumer_support_by_id_string(id_string):
    try:
        return ConsumerSupport.objects.get(id_string = id_string)
    except:
        return False

def get_consumer_support_by_tenant_id_string(id_string):
    return ConsumerSupport.objects.filter(tenant__id_string = id_string)


def get_consumer_sub_support_by_id(id):
    try:
        return ConsumerSupport.objects.get(id = id)
    except:
        return False

# End the Code