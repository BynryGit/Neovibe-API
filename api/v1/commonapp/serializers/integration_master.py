from rest_framework import serializers, status
from v1.commonapp.models.integration_master import IntegrationMaster as IntegrationMasterTbl
from v1.commonapp.serializers.integration_subtype import IntegrationSubTypeListSerializer
from v1.utility.serializers.utility_module import UtilityModuleShortViewSerializer
from datetime import datetime
from django.db import transaction
from api.messages import INTEGRATION_MASTER_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.commonapp.common_functions import set_integration_master_validated_data


class IntegrationMasterListSerializer(serializers.ModelSerializer):
    integration_sub_type = IntegrationSubTypeListSerializer(source='get_integration_sub_type')
    utility_module = UtilityModuleShortViewSerializer(source='get_utility_module')

    class Meta:
        model = IntegrationMasterTbl
        fields = (
            'name', 'id_string', 'integration_sub_type', 'utility_module', 'is_active', 'created_by', 'created_date')


class IntegrationMasterViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = IntegrationMasterTbl
        fields = (
            'tenant', 'tenant_id_string', 'utility', 'utility_id_string', 'name', 'id_string')


class IntegrationMasterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    integration_type_id = serializers.CharField(required=False, max_length=200)
    integration_sub_type_id = serializers.CharField(required=False, max_length=200)
    module_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = IntegrationMasterTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_integration_master_validated_data(validated_data)
            if IntegrationMasterTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                                   utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(INTEGRATION_MASTER_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:
                integration_obj = super(IntegrationMasterSerializer, self).create(validated_data)
                integration_obj.created_by = user.id
                integration_obj.save()
                return integration_obj

    def update(self, instance, validated_data, user):
        validated_data = set_integration_master_validated_data(validated_data)
        if IntegrationMasterTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                               utility_id=validated_data['utility_id']).exists():
            raise CustomAPIException(INTEGRATION_MASTER_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
        else:
            with transaction.atomic():
                integration_obj = super(IntegrationMasterSerializer, self).update(instance, validated_data)
                integration_obj.updated_by = user.id
                integration_obj.updated_date = datetime.utcnow()
                integration_obj.save()
                return integration_obj
