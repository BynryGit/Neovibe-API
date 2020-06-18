__author__ = "Arpita"

from datetime import datetime
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.userapp.models.user_status import UserStatus
from v1.utility.serializers.utility import UtilitySerializer


class GetUserStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserStatus
        fields = ('status', 'id_string')


class UserStatusListSerializer(serializers.ModelSerializer):
    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = UserStatus
        fields = ('id_string', 'tenant', 'utility', 'status', 'is_active')


class UserStatusViewSerializer(serializers.ModelSerializer):
    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = UserStatus
        fields = ('id_string', 'tenant', 'utility', 'status', 'is_active')


class UserStatusSerializer(serializers.ModelSerializer):
    status = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UserStatus
        validators = [UniqueTogetherValidator(queryset=UserStatus.objects.all(), fields=('status',), message='User Status already exists!')]
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            status_obj = super(UserStatusSerializer, self).create(validated_data)
            status_obj.created_by = user.id
            status_obj.updated_by = user.id
            status_obj.created_date = datetime.utcnow()
            status_obj.updated_date = datetime.utcnow()
            status_obj.tenant = user.tenant
            status_obj.utility = user.utility
            status_obj.is_active = True
            status_obj.save()
            return status_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            status_obj = super(UserStatusSerializer, self).update(instance, validated_data)
            status_obj.updated_by = user.id
            status_obj.updated_date = datetime.utcnow()
            status_obj.is_active = True
            status_obj.save()
            return status_obj
