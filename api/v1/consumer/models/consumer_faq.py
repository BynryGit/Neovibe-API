import uuid  # importing package for guid
from datetime import datetime # importing package for datetime

from django.db import models  # importing package for database

# Create Consumer FAQ table start
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.consumer.models.consumer_sub_category import get_consumer_sub_category_by_id
from v1.consumer.models.consumer_category import get_consumer_category_by_id
from django.contrib.postgres.fields import JSONField
from django.utils import timezone # importing package for datetime


class ConsumerFaq(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    question = models.CharField(max_length=200, blank=False, null=False)
    answer = models.CharField(max_length=200, blank=True, null=True)
    category_id = models.BigIntegerField(blank=True, null=True)
    subcategory_id = models.BigIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=timezone.now)
    updated_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.question

    def __unicode__(self):
        return self.question
    
    @property
    def get_category_subtype(self):
        consumer_sub_category = get_consumer_sub_category_by_id(self.subcategory_id)
        return consumer_sub_category
    
    @property
    def get_category_type(self):
        consumer_category = get_consumer_category_by_id(self.category_id)
        return consumer_category

# Create Consumer FAQ table end

def get_consumer_faq_by_id_string(id_string):
    try:
        return ConsumerFaq.objects.get(id_string = id_string)
    except:
        return False

def get_faq_by_tenant_id_string(id_string):
    return ConsumerFaq.objects.filter(tenant__id_string = id_string)


def get_consumer_faq_by_id(id):
    try:
        return ConsumerFaq.objects.filter(id = id)
    except:
        return False

# End the Code