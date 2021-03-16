__author__ = "chinmay"

from rest_framework import serializers, status
from v1.commonapp.models.department_subtype import DepartmentSubtype as DepartmentSubtypeTbl
from django.db import transaction
from v1.commonapp.common_functions import set_department_subtype_validated_data
from datetime import datetime
from api.messages import DEPARTMENT_SUBTYPE_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.utility.models.utility_department_subtype import UtilityDepartmentSubType as UtilityDepartmentSubTypeTbl


class DepartmentSubTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = UtilityDepartmentSubTypeTbl
        fields = '__all__'


class DepartmentSubTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    department_subtype_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UtilityDepartmentSubTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_department_subtype_validated_data(validated_data)
            if UtilityDepartmentSubTypeTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                                          utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(DEPARTMENT_SUBTYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                department_subtype_obj = super(DepartmentSubTypeSerializer, self).create(validated_data)
                department_subtype_obj.created_by = user.id
                department_subtype_obj.save()
                return department_subtype_obj

    def update(self, instance, validated_data, user):
        validated_data = set_department_subtype_validated_data(validated_data)
        if UtilityDepartmentSubTypeTbl.objects.filter(name=validated_data['name'],
                                                      tenant_id=validated_data['tenant_id'],
                                                      utility_id=validated_data['utility_id']).exists():
            raise CustomAPIException(DEPARTMENT_SUBTYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                department_subtype_obj = super(DepartmentSubTypeSerializer, self).update(instance, validated_data)
                department_subtype_obj.tenant = user.tenant
                department_subtype_obj.updated_by = user.id
                department_subtype_obj.updated_date = datetime.utcnow()
                department_subtype_obj.save()
                return department_subtype_obj


class DepartmentSubTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentSubtypeTbl
        fields = ('name', 'id_string', 'is_active', 'created_by', 'created_date')