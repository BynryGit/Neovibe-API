__author__ = "Arpita"

from datetime import datetime
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from v1.tenant.serializers.tenant import GetTenantSerializer
from v1.userapp.models.user_type import UserType
from v1.utility.serializers.utility import UtilitySerializer


class GetUserTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserType
        fields = ('name', 'id_string')


class UserTypeListSerializer(serializers.ModelSerializer):
    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = UserType
        fields = ('id_string', 'tenant', 'utility', 'name', 'is_active')


class UserTypeViewSerializer(serializers.ModelSerializer):
    tenant = GetTenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')

    class Meta:
        model = UserType
        fields = ('id_string', 'tenant', 'utility', 'name', 'is_active')


class UserTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UserType
        validators = [UniqueTogetherValidator(queryset=UserType.objects.all(), fields=('name',), message='User Type already exists!')]
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            sub_type_obj = super(UserTypeSerializer, self).create(validated_data)
            sub_type_obj.created_by = user.id
            sub_type_obj.created_date = datetime.utcnow()
            sub_type_obj.tenant = user.tenant
            sub_type_obj.utility = user.utility
            sub_type_obj.is_active = True
            sub_type_obj.save()
            return sub_type_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            sub_type_obj = super(UserTypeSerializer, self).update(instance, validated_data)
            sub_type_obj.updated_by = user.id
            sub_type_obj.updated_date = datetime.utcnow()
            sub_type_obj.is_active = True
            sub_type_obj.save()
            return sub_type_obj
