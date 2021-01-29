__author__ = "Arpita"

from datetime import datetime

from django.db import transaction
from rest_framework import serializers

from v1.commonapp.views.settings_reader import SettingReader
setting_reader = SettingReader()
from v1.commonapp.models.document import Document
from v1.commonapp.serializers.document_sub_type import DocumentSubTypeSerializer
from v1.commonapp.serializers.document_type import DocumentTypeSerializer
from v1.commonapp.serializers.module import ModuleSerializer
from v1.commonapp.serializers.sub_module import SubModuleSerializer
from v1.tenant.serializers.tenant_status import TenantStatusViewSerializer
from v1.userapp.serializers.user import UserSerializer
from v1.userapp.views.common_functions import set_document_validated_data
from v1.utility.serializers.utility import UtilitySerializer


class DocumentViewSerializer(serializers.ModelSerializer):

    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    module = ModuleSerializer(many=False, required=True, source='get_module')
    sub_module = SubModuleSerializer(many=False, required=True, source='get_sub_module')
    document_type = DocumentTypeSerializer(many=False, required=True, source='get_type')
    document_sub_type = DocumentSubTypeSerializer(many=False, required=True, source='get_sub_type')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = Document
        fields = ('id_string', 'name', 'link', 'created_date', 'updated_date', 'tenant', 'utility', 'module',
                  'sub_module', 'document_type', 'document_sub_type')


class DocumentSerializer(serializers.ModelSerializer):
    utility_id = serializers.CharField( required=True, max_length=200)
    module_id = serializers.CharField( required=True, max_length=200)
    sub_module_id = serializers.CharField(required=True, max_length=200)
    document_type_id = serializers.CharField(required=True, max_length=200)
    document_sub_type_id = serializers.CharField(required=True, max_length=200)
    identification_id = serializers.CharField(required=True, max_length=200)
    name = serializers.CharField(required=True, max_length=200)
    link = serializers.CharField(required=True, max_length=200)

    class Meta:
        model = Document
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data =  set_document_validated_data(validated_data)
        with transaction.atomic():
            document_obj = super(DocumentSerializer, self).create(validated_data)
            document_obj.created_by = user.id
            document_obj.updated_by = user.id
            document_obj.created_date = datetime.utcnow()
            document_obj.updated_date = datetime.utcnow()
            document_obj.tenant = user.tenant
            document_obj.is_active = True
            document_obj.save()
            return document_obj

    def update(self, instance, validated_data, user):
        validated_data = set_document_validated_data(validated_data)
        with transaction.atomic():
            document_obj = super(DocumentSerializer, self).update(instance, validated_data)
            document_obj.updated_by = user.id
            document_obj.updated_date = datetime.utcnow()
            document_obj.is_active = True
            document_obj.save()
            return document_obj


class DocumentListSerializer(serializers.ModelSerializer):

    tenant = TenantStatusViewSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    module = ModuleSerializer(many=False, required=True, source='get_module')
    sub_module = SubModuleSerializer(many=False, required=True, source='get_sub_module')
    document_type = DocumentTypeSerializer(many=False, required=True, source='get_type')
    document_sub_type = DocumentSubTypeSerializer(many=False, required=True, source='get_sub_type')
    identification = UserSerializer(many=False, required=True, source='get_user_identification')
    created_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)
    updated_date = serializers.DateTimeField(format=setting_reader.get_display_date_format(), read_only=True)

    class Meta:
        model = Document
        fields = ('id_string', 'tenant', 'utility', 'module', 'sub_module', 'document_type', 'document_sub_type',
                  'identification', 'name', 'link', 'created_date', 'updated_date')
