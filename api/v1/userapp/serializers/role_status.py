__author__ = "Arpita"

from datetime import datetime
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from v1.tenant.serializers.tenant import GetTenantSerializer
from v1.userapp.models.role_status import RoleStatus
from v1.utility.serializers.utility import UtilitySerializer


class GetRoleStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = RoleStatus
        fields = ('status', 'id_string')


class RoleStatusListSerializer(serializers.ModelSerializer):
    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = RoleStatus
        fields = ('id_string', 'tenant', 'utility', 'status', 'is_active')


class RoleStatusViewSerializer(serializers.ModelSerializer):
    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = RoleStatus
        fields = ('id_string', 'tenant', 'utility', 'status', 'is_active')


class RoleStatusSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = RoleStatus
        validators = [UniqueTogetherValidator(queryset=RoleStatus.objects.all(), fields=('status',), message='Role Status already exists!')]
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            sub_type_obj = super(RoleStatusSerializer, self).create(validated_data)
            sub_type_obj.created_by = user.id
            sub_type_obj.created_date = datetime.utcnow()
            sub_type_obj.tenant = user.tenant
            sub_type_obj.utility = user.utility
            sub_type_obj.is_active = True
            sub_type_obj.save()
            return sub_type_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            sub_type_obj = super(RoleStatusSerializer, self).update(instance, validated_data)
            sub_type_obj.updated_by = user.id
            sub_type_obj.updated_date = datetime.utcnow()
            sub_type_obj.is_active = True
            sub_type_obj.save()
            return sub_type_obj
