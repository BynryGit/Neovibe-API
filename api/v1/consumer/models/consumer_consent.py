import uuid  # importing package for guid
from datetime import datetime # importing package for datetime
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from django.db import models  # importing package for database
from v1.consumer.models.consumer_category import get_consumer_category_by_id
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id
from django.utils import timezone # importing package for datetime


# Create Consumer Category table start



class ConsumerConsent(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=True, null=True)
    consumer_category_id = models.BigIntegerField(null=True, blank=True)
    consumer_subcategory_id = models.BigIntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
    
    @property
    def get_consumer_category(self):
        consumer_category = get_consumer_category_by_id(self.consumer_category_id)
        return consumer_category
    
    @property
    def get_consumer_subcategory(self):
        consumer_subcategory = get_consumer_sub_category_by_id(self.consumer_subcategory_id)
        return consumer_subcategory

# Create Consumer Category table end

def get_consumer_consent_by_tenant_id_string(id_string):
    return ConsumerConsent.objects.filter(tenant__id_string = id_string)

def get_consumer_consent_by_id_string(id_string):
    try:
        return ConsumerConsent.objects.get(id_string=id_string)
    except:
        return False


def get_consumer_consent_by_id(id):
    try:
        return ConsumerConsent.objects.filter(id = id)
    except:
        return False

# End The Code