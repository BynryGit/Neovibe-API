__author__ = "Arpita"

from rest_framework import serializers

from v1.commonapp.models.document import Document
from v1.commonapp.serializers.document_sub_type import DocumentSubTypeSerializer
from v1.commonapp.serializers.document_type import DocumentTypeSerializer
from v1.commonapp.serializers.module import ModuleSerializer
from v1.commonapp.serializers.sub_module import SubModuleSerializer
from v1.tenant.serializers.tenant import TenantSerializer
from v1.userapp.serializers.user import UserSerializer
from v1.utility.serializers.utility import UtilitySerializer


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