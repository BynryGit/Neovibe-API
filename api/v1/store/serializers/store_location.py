from rest_framework import serializers, status
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.store.models.store_location import StoreLocation as StoreLocationTbl
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import NAME_ALREADY_EXIST
from v1.store.views.common_functions import set_store_type_vaidated_data
from v1.commonapp.serializers.city import CityListSerializer
from v1.commonapp.serializers.area import AreaListSerializer


class StoreLocationListSerializer(serializers.ModelSerializer):
    city=CityListSerializer(many=False, source='get_city')
    area=AreaListSerializer(many=False, source='get_area')

    class Meta:
        model = StoreLocationTbl
        fields = ('id_string', 'store_id','store_name','store_address','latitude','longitude','city','area','is_active','created_by','created_date')

class StoreLocationViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = StoreLocationTbl
        fields = ('id_string', 'store_id','store_name', 'tenant','tenant_id_string','utility','utility_id_string')


class StoreLocationSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(required=True, max_length=200)
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = StoreLocationTbl
        fields = ('__all__')

    def create(self, validated_data,  user):
        with transaction.atomic():
            validated_data = set_store_type_vaidated_data(validated_data)
            if StoreLocationTbl.objects.filter(store_name=validated_data['store_name'],tenant_id=validated_data['tenant_id'],
                                            utility_id=validated_data['utility_id']).exists():
                    raise CustomAPIException(NAME_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                store_location_obj = super(StoreLocationSerializer, self).create(validated_data)
                store_location_obj.created_by = user.id
                store_location_obj.updated_by = user.id
                store_location_obj.save()
                return store_location_obj

    def update(self, instance, validated_data, user):
        validated_data = set_store_type_vaidated_data(validated_data)
        if StoreLocationTbl.objects.filter(store_name=validated_data['store_name'],tenant_id=validated_data['tenant_id'],
                                            utility_id=validated_data['utility_id']).exists():
                    raise CustomAPIException(NAME_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                store_location_obj = super(StoreLocationSerializer, self).update(instance, validated_data)
                store_location_obj.updated_by = user.id
                store_location_obj.updated_date = datetime.utcnow()
                store_location_obj.save()
                return store_location_obj
