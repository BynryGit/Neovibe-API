__author__ = "aki"

from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from v1.utility.models.utility_master import UtilityMaster as UtilityMasterTbl


class UtilitySerializer(serializers.ModelSerializer):

    class Meta:
        model = UtilityMasterTbl
        fields = ('name', 'id_string')


class UtilityMasterViewSerializer(serializers.ModelSerializer):
    tenant_name = serializers.ReadOnlyField(source='tenant.name')

    class Meta:
        model = UtilityMasterTbl
        fields = ('id_string', 'tenant_name', 'short_name', 'name', 'phone_no', 'email_id')


class UtilityMasterSerializer(serializers.ModelSerializer):
    tenant_id_string = serializers.UUIDField(required=True, source='tenant.id_string')

    class Meta:
        model = UtilityMasterTbl
        fields = ('tenant_id_string', 'short_name', 'name', 'phone_no', 'email_id', 'region_id', 'country_id', 'state_id',
                  'city_id', 'status_id', 'created_by')

    def create(self, validated_data, user):
        with transaction.atomic():
            utility_obj = super(UtilityMasterSerializer, self).create(validated_data)
            utility_obj.created_by = user
            utility_obj.save()
            return utility_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            utility_obj = super(UtilityMasterSerializer, self).update(instance, validated_data)
            utility_obj.updated_by = user
            utility_obj.updated_date=timezone.now()
            utility_obj.save()
            return utility_obj