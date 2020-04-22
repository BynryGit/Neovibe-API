import datetime
import uuid

from django.db import models
# Remove all fields as compulsory
# Create Consumer Registration table start.
class ConsumerRegistration(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant_id = models.IntegerField(null=False, blank=False)
    utility_id = models.IntegerField(null=False, blank=False)
    registration_no = models.IntegerField(null=False, blank=False)
    registration_type_id = models.CharField(null=True, blank=True)
    status_id = models.CharField(null=True, blank=True)
    first_name = models.CharField(null=True, blank=True)
    middle_name = models.CharField(null=True, blank=True)
    last_name = models.CharField(null=True, blank=True)
    email_id = models.CharField(null=True, blank=True)
    phone_mobile = models.IntegerField(null=True, blank=True)
    phone_landline = models.IntegerField(null=True, blank=True)
    address_line_1 = models.CharField(null=True, blank=True)
    street = models.CharField(null=True, blank=True)
    zipcode = models.IntegerField(null=True, blank=True)
    country_id = models.CharField(null=True, blank=True)
    state_id = models.CharField(null=True, blank=True)
    city_id = models.CharField(null=True, blank=True)
    area_id = models.CharField(null=True, blank=True)
    subarea_id = models.CharField(null=True, blank=True)
    scheme_id = models.CharField(null=True, blank=True)
    payment_id = models.CharField(null=True, blank=True)
    ownership_id = models.CharField(null=True, blank=True)
    consumer_category_id = models.CharField(null=True, blank=True)
    sub_category_id = models.CharField(null=True, blank=True)
    is_vip = models.BooleanField(default=False)
    connectivity = models.BooleanField(default=False)
    registration_channel_id = models.CharField(null=True, blank=True)
    source_id = models.CharField(null=False, blank=False)
    registration_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=True, blank=True)
    updated_by = models.IntegerField(null=True, blank=True)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.registration_no

    def __unicode__(self):
        return self.registration_no