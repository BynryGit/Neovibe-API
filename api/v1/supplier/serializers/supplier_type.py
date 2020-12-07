from rest_framework import serializers, status
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.supplier.models.supplier_type import SupplierType as SupplierTypeTbl
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import NAME_ALREADY_EXIST
from v1.supplier.views.common_functions import set_supplier_type_vaidated_data

class SupplierTypeListSerializer(serializers.ModelSerializer):

    class Meta:
        model = SupplierTypeTbl
        fields = ('id_string', 'name','is_active','created_by','created_date')

class SupplierTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = SupplierTypeTbl
        fields = ('id_string', 'name', 'tenant','tenant_id_string','utility','utility_id_string')


class SupplierTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200)
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = SupplierTypeTbl
        fields = ('__all__')

    def create(self, validated_data,  user):
        with transaction.atomic():
            validated_data = set_supplier_type_vaidated_data(validated_data)
            if SupplierTypeTbl.objects.filter(name=validated_data['name'],tenant_id=validated_data['tenant_id'],
                                            utility_id=validated_data['utility_id']).exists():
                    raise CustomAPIException(NAME_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                supplier_type_obj = super(SupplierTypeSerializer, self).create(validated_data)
                supplier_type_obj.created_by = user.id
                supplier_type_obj.updated_by = user.id
                supplier_type_obj.save()
                return supplier_type_obj

    def update(self, instance, validated_data, user):
        validated_data = set_supplier_type_vaidated_data(validated_data)
        if SupplierTypeTbl.objects.filter(name=validated_data['name'],tenant_id=validated_data['tenant_id'],
                                            utility_id=validated_data['utility_id']).exists():
                    raise CustomAPIException(NAME_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                supplier_type_obj = super(SupplierTypeSerializer, self).update(instance, validated_data)
                supplier_type_obj.updated_by = user.id
                supplier_type_obj.updated_date = datetime.utcnow()
                supplier_type_obj.save()
                return supplier_type_obj