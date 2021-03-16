from rest_framework import serializers, status
from v1.commonapp.models.division import Division as DivisionTbl
from v1.commonapp.serializers.country import CountryListSerializer, CountryViewSerializer
from v1.commonapp.serializers.zone import ZoneListSerializer
from v1.commonapp.common_functions import set_division_validated_data
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import DIVISION_ALREADY_EXIST
from datetime import datetime
from django.db import transaction


class DivisionViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = DivisionTbl
        fields = (
            'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'id_string')


class DivisionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    zone_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = DivisionTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_division_validated_data(validated_data)
            if DivisionTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                          utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(DIVISION_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                division_obj = super(DivisionSerializer, self).create(validated_data)
                division_obj.created_by = user.id
                division_obj.save()
                return division_obj

    def update(self, instance, validated_data, user):
        validated_data = set_division_validated_data(validated_data)
        if DivisionTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                      utility_id=validated_data['utility_id']).exists():
            raise CustomAPIException(DIVISION_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                division_obj = super(DivisionSerializer, self).update(instance, validated_data)
                division_obj.updated_by = user.id
                division_obj.updated_date = datetime.utcnow()
                division_obj.save()
                return division_obj


class DivisionListSerializer(serializers.ModelSerializer):
    zone_id = ZoneListSerializer(source="get_zone")

    class Meta:
        model = DivisionTbl
        fields = ('name', 'id_string', 'zone_id', 'created_date', 'is_active', 'created_by')
