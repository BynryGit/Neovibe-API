import uuid  # importing package for guid
from datetime import datetime  # importing package for datetime
from django.db import models  # importing package for database
from v1.tenant.models.tenant_master import TenantMaster
from v1.utility.models.utility_master import UtilityMaster
from v1.commonapp.models.region import get_region_by_id
from v1.commonapp.models.country import get_country_by_id
from v1.commonapp.models.state import get_state_by_id
from v1.commonapp.models.city import get_city_by_id
from v1.commonapp.models.zone import get_zone_by_id
from v1.commonapp.models.area import get_area_by_id
from v1.commonapp.models.sub_area import get_sub_area_by_id


# Create Premises table start


class Premise(models.Model):
    id_string = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    tenant = models.ForeignKey(TenantMaster, blank=True, null=True, on_delete=models.SET_NULL)
    utility = models.ForeignKey(UtilityMaster, blank=True, null=True, on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, blank=False, null=False)
    MRU = models.CharField(max_length=200, blank=True, null=True)
    GIS = models.CharField(max_length=200, blank=True, null=True)
    premises_address = models.CharField(max_length=200, blank=True, null=True)
    region_id = models.BigIntegerField(blank=True, null=True)
    country_id = models.BigIntegerField(blank=True, null=True)
    state_id = models.BigIntegerField(blank=True, null=True)
    city_id = models.BigIntegerField(blank=True, null=True)
    zone_id = models.BigIntegerField(blank=True, null=True)
    area_id = models.BigIntegerField(blank=True, null=True)
    subarea_id = models.BigIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_by = models.BigIntegerField(null=True, blank=True)
    updated_by = models.BigIntegerField(null=True, blank=True)
    created_date = models.DateTimeField(null=True, blank=True, default=datetime.now())
    updated_date = models.DateTimeField(null=True, blank=True, default=datetime.now())

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name
    
    @property
    def get_region(self):
        region = get_region_by_id(self.region_id)
        return region
    
    @property
    def get_country(self):
        country = get_country_by_id(self.country_id)
        return country

    @property
    def get_state(self):
        state = get_state_by_id(self.state_id)
        return state
    
    @property
    def get_city(self):
        city = get_city_by_id(self.city_id)
        return city
    
    @property
    def get_zone(self):
        zone = get_zone_by_id(self.zone_id)
        return zone

    @property
    def get_area(self):
        area = get_area_by_id(self.area_id)
        return area
    
    @property
    def get_sub_area(self):
        subarea = get_sub_area_by_id(self.subarea_id)
        return subarea


# Create Zone table end


def get_premise_by_id_string(id_string):
    try:
        return Premise.objects.get(id_string=id_string)
    except:
        return False


def get_premise_by_id(id):
    return Premise.objects.filter(id=id)

# End the Code