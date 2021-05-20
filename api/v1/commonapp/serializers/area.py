from rest_framework import serializers, status
from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.commonapp.models.area import Area as AreaTbl
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.utility.serializers.utility import UtilitySerializer
from v1.commonapp.serializers.division import DivisionListSerializer
from datetime import datetime
from django.db import transaction
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.common_functions import set_area_validated_data
from api.messages import AREA_ALREADY_EXIST


class AreaShortViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = AreaTbl
        fields = ('id_string',)


class AreaViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')
    

    class Meta:
        model = AreaTbl
        fields = (
            'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'id_string')


class AreaSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    division_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = AreaTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_area_validated_data(validated_data)
            if AreaTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                      utility_id=validated_data['utility_id'],division_id=validated_data['division_id']).exists():
                raise CustomAPIException(AREA_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                area_obj = super(AreaSerializer, self).create(validated_data)
                area_obj.created_by = user.id
                area_obj.save()
                return area_obj

    def update(self, instance, validated_data, user):
        validated_data = set_area_validated_data(validated_data)
        if AreaTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                  utility_id=validated_data['utility_id'],division_id=validated_data['division_id']).exists():
            raise CustomAPIException(AREA_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                area_obj = super(AreaSerializer, self).update(instance, validated_data)
                area_obj.updated_by = user.id
                area_obj.updated_date = datetime.utcnow()
                area_obj.save()
                return area_obj


class AreaListSerializer(serializers.ModelSerializer):
    division = DivisionListSerializer(source="get_division")

    class Meta:
        model = AreaTbl
        fields = ('name', 'id_string', 'division','created_date')
