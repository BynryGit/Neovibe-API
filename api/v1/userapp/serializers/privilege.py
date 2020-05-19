__author__ = "Arpita"

from datetime import datetime

from django.db import transaction
from rest_framework import serializers

from v1.userapp.models.privilege import Privilege


class PrivilegeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = Privilege
        depth = 1
        fields = ('id_string', 'tenant', 'utility', 'name', 'created_date')


class PrivilegeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = Privilege
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            privilege_obj = super(PrivilegeSerializer, self).create(validated_data)
            privilege_obj.created_by = user.id
            privilege_obj.created_date = datetime.utcnow()
            privilege_obj.tenant = user.tenant
            privilege_obj.utility = user.utility
            privilege_obj.is_active = True
            privilege_obj.save()
            return privilege_obj

    def update(self, instance, validated_data, user):
        with transaction.atomic():
            role_obj = super(PrivilegeSerializer, self).update(instance, validated_data)
            role_obj.updated_by = user.id
            role_obj.updated_date = datetime.utcnow()
            role_obj.save()
            return role_obj


class PrivilegeViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Privilege
        depth = 1
        fields = ('id_string', 'tenant', 'utility', 'name', 'created_date', 'is_active')
