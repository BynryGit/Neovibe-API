__author__ = "arpita"

from rest_framework import serializers, status
from v1.commonapp.models.department import Department as DepartmentTbl
from django.db import transaction
from v1.commonapp.common_functions import set_department_type_validated_data
from datetime import datetime
from api.messages import DEPARTMENT_TYPE_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.utility.models.utility_department_type import UtilityDepartmentType as UtilityDepartmentTypeTbl


class DepartmentViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = UtilityDepartmentTypeTbl
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    department_type_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UtilityDepartmentTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_department_type_validated_data(validated_data)
            if UtilityDepartmentTypeTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                                        utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(DEPARTMENT_TYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                department_type_obj = super(DepartmentSerializer, self).create(validated_data)
                department_type_obj.created_by = user.id
                department_type_obj.updated_by = user.id
                department_type_obj.save()
                return department_type_obj

    def update(self, instance, validated_data, user):
        validated_data = set_department_type_validated_data(validated_data)
        with transaction.atomic():
            department_type_obj = super(DepartmentSerializer, self).update(instance, validated_data)
            department_type_obj.tenant = user.tenant
            department_type_obj.updated_by = user.id
            department_type_obj.updated_date = datetime.utcnow()
            department_type_obj.save()
            return department_type_obj


class DepartmentListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepartmentTbl
        fields = ('name', 'id_string', 'is_active', 'created_by', 'created_date')
