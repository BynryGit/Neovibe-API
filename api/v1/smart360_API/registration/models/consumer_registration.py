import datetime
import uuid

from django.db import models
# Remove all fields as compulsory
# Create Consumer Registration table start.
class ConsumerRegistration(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant_id = models.IntegerField(null=False, blank=False) #Table name, Foreign key need to be added.
    utility_id = models.IntegerField(null=False, blank=False)  #Table name, Foreign key need to be added.
    registration_no = models.IntegerField(null=False, blank=False) #Change to Alphanumeric
    registration_type_id = models.IntegerField(null=False, blank=False)
    status_id = models.IntegerField(null=False, blank=False)
    first_name = models.CharField(null=False, blank=False)
    middle_name = models.CharField(null=False, blank=False) # make null true
    last_name = models.CharField(null=False, blank=False)
    email_id = models.CharField(null=False, blank=False)
    phone_no1 = models.IntegerField(null=False, blank=False) #TODO: CharField, phone_mobile
    phone_no2 = models.IntegerField(null=False, blank=False) #TODO: CharField,phone_landline
    Address_ln1 = models.CharField(null=False, blank=False) #small
    street = models.CharField(null=False, blank=False)
    Zipcode_id = models.IntegerField(null=False, blank=False) #small, need to be only zipcode
    country_id = models.IntegerField(null=False, blank=False)
    state_id = models.IntegerField(null=False, blank=False)
    city_id = models.IntegerField(null=False, blank=False)
    area_id = models.IntegerField(null=False, blank=False)
    subarea_id = models.IntegerField(null=False, blank=False)
    scheme_id = models.IntegerField(null=False, blank=False)
    payment_id = models.IntegerField(null=False, blank=False)
    ownership_id = models.IntegerField(null=False, blank=False)
    consumer_category_id = models.IntegerField(null=False, blank=False)
    sub_category_id = models.IntegerField(null=False, blank=False)
    vip = models.BooleanField(default=False)#Change to is_vip
    pipeline = models.BooleanField(default=False) #Change to is_connectivity
    registration_channel_id = models.IntegerField(null=False, blank=False)
    source_id = models.IntegerField(null=False, blank=False)
    registration_date = models.DateField(null=True, blank=True, default=datetime.now())
    is_active = models.BooleanField(default=False)
    created_by = models.IntegerField(null=False, blank=False)
    updated_by = models.IntegerField(null=False, blank=False)
    created_date = models.DateField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.registration_no

    def __unicode__(self):
        return self.registration_no