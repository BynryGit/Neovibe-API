__author__ = "aki"

from rest_framework import serializers
from v1.tenant.models.tenant_region import TenantRegion as TenantRegionTbl
from v1.commonapp.models.region import Region
from django.db import transaction
from v1.consumer.views.common_functions import set_validated_data


class TenantRegionSerializer(serializers.ModelSerializer):

    class Meta:
        model = TenantRegionTbl
        fields = ('id_string', 'region')
    

class RegionViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
  

    class Meta:
        model = Region
        fields = ('__all__')
    

# class RegionSerializer(serializers.ModelSerializer):
#     utility_id = serializers.CharField(required=False, max_length=200)
#     tenant_id = serializers.CharField(required=False, max_length=200)

#     class Meta:
#         model = Region
#         fields = ('__all__')
    
#     def create(self, validated_data, user):
#         validated_data =  set_validated_data(validated_data)
#         with transaction.atomic():
#             region_obj = super(RegionSerializer, self).create(validated_data)
#             region_obj.created_by = user.id
#             region_obj.save()
#             return region_obj

class RegionSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = Region
        fields = ('__all__')


class RegionListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Region
        fields = ('name', 'id_string','key')
    
   
