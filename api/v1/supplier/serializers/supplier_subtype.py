from rest_framework import serializers, status
from v1.commonapp.serializers.tenant import TenantMasterViewSerializer
from v1.commonapp.serializers.utility import UtilityMasterViewSerializer
from v1.supplier.models.supplier_subtype import SupplierSubType as SupplierSubTypeTbl
from django.db import transaction
from datetime import datetime
from v1.commonapp.views.custom_exception import CustomAPIException
from api.messages import NAME_ALREADY_EXIST
from v1.supplier.serializers.supplier_type import SupplierTypeListSerializer
from v1.supplier.views.common_functions import set_supplier_subtype_vaidated_data


class SupplierSubTypeListSerializer(serializers.ModelSerializer):
    supplier_type=SupplierTypeListSerializer(many=False, source='get_supplier_type')

    class Meta:
        model = SupplierSubTypeTbl
        fields = ('id_string', 'name','is_active','created_by','created_date','supplier_type')

class SupplierSubTypeViewSerializer(serializers.ModelSerializer):
    supplier_type=SupplierTypeListSerializer(many=False, source='get_supplier_type')
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = SupplierSubTypeTbl
        fields = ('id_string', 'name', 'tenant','tenant_id_string','utility','utility_id_string','supplier_type')

class SupplierSubTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200)
    supplier_type_id=serializers.CharField(required=True, max_length=200)
    utility_id = serializers.CharField(required=True, max_length=200)
    tenant_id = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = SupplierSubTypeTbl
        fields = ('__all__')

    def create(self, validated_data,  user):
        with transaction.atomic():
            validated_data = set_supplier_subtype_vaidated_data(validated_data)
            if SupplierSubTypeTbl.objects.filter(name=validated_data['name'],tenant_id=validated_data['tenant_id'],
                                            utility_id=validated_data['utility_id']).exists():
                    raise CustomAPIException(NAME_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                supplier_subtype_obj = super(SupplierSubTypeSerializer, self).create(validated_data)
                supplier_subtype_obj.created_by = user.id
                supplier_subtype_obj.updated_by = user.id
                supplier_subtype_obj.save()
                return supplier_subtype_obj

    def update(self, instance, validated_data, user):
        validated_data = set_supplier_subtype_vaidated_data(validated_data)
        if SupplierSubTypeTbl.objects.filter(name=validated_data['name'],tenant_id=validated_data['tenant_id'],
                                            utility_id=validated_data['utility_id']).exists():
                    raise CustomAPIException(NAME_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                supplier_subtype_obj = super(SupplierSubTypeSerializer, self).update(instance, validated_data)
                supplier_subtype_obj.updated_by = user.id
                supplier_subtype_obj.updated_date = datetime.utcnow()
                supplier_subtype_obj.save()
                return supplier_subtype_obj
