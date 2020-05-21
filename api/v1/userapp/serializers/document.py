__author__ = "Arpita"
from django.db import transaction
from rest_framework import serializers

from v1.commonapp.models.document import Document
from v1.commonapp.serializers.document_sub_type import DocumentSubTypeSerializer
from v1.commonapp.serializers.document_type import DocumentTypeSerializer
from v1.commonapp.serializers.module import ModuleSerializer
from v1.commonapp.serializers.sub_module import SubModuleSerializer
from v1.tenant.serializers.tenant import TenantSerializer
from v1.userapp.serializers.user import UserSerializer
from v1.userapp.views.common_functions import set_document_validated_data
from v1.utility.serializers.utility import UtilitySerializer


class DocumentViewSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    module = ModuleSerializer(many=False, required=True, source='get_module')
    sub_module = SubModuleSerializer(many=False, required=True, source='get_sub_module')
    document_type = DocumentTypeSerializer(many=False, required=True, source='get_type')
    document_sub_type = DocumentSubTypeSerializer(many=False, required=True, source='get_sub_type')

    class Meta:
        model = Document
        fields = ('id_string', 'tenant', 'utility', 'module', 'sub_module', 'document_type', 'document_sub_type',
                  'name', 'link', 'is_active', 'created_by')


class DocumentSerializer(serializers.ModelSerializer):
    module_id = serializers.CharField( required=False, max_length=200)
    sub_module_id = serializers.CharField(required=False, max_length=200)
    document_type_id = serializers.CharField(required=False, max_length=200)
    document_sub_type_id = serializers.CharField(required=False, max_length=200)
    identification_id = serializers.CharField(required=False, max_length=200)
    name = serializers.CharField(required=False, max_length=200)
    link = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = Document
        fields = '__all__'

    def create(self, validated_data, user):
        validated_data =  set_document_validated_data(validated_data)
        with transaction.atomic():
            document = super(DocumentSerializer, self).create(validated_data)
            document.created_by = user.id
            document.tenant = user.tenant
            document.utility = user.utility
            document.is_active = True
            document.save()
            return document


class DocumentListSerializer(serializers.ModelSerializer):
    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    module = ModuleSerializer(many=False, required=True, source='get_module')
    sub_module = SubModuleSerializer(many=False, required=True, source='get_sub_module')
    document_type = DocumentTypeSerializer(many=False, required=True, source='get_type')
    document_sub_type = DocumentSubTypeSerializer(many=False, required=True, source='get_sub_type')
    identification = UserSerializer(many=False, required=True, source='get_user_identification')

    class Meta:
        model = Document
        fields = ('id_string', 'tenant', 'utility', 'module', 'sub_module', 'document_type', 'document_sub_type',
                  'identification', 'name', 'link', 'is_active', 'created_by')
