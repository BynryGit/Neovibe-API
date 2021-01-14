__author__ = "Priyanka"

from rest_framework import serializers
from v1.commonapp.models.document import Document as DocumentTbl
from v1.commonapp.serializers.document_sub_type import DocumentSubTypeSerializer
from v1.commonapp.serializers.document_type import DocumentTypeSerializer
from v1.tenant.serializers.tenant import TenantSerializer
from v1.utility.serializers.utility import UtilitySerializer
from api.settings.prod import DISPLAY_DATE_TIME_FORMAT

class DocumentSerializer(serializers.ModelSerializer):
    def get_created_date(self, obj):
        return obj.created_date.strftime(DISPLAY_DATE_TIME_FORMAT)

    tenant = TenantSerializer(many=False, required=True, source='get_tenant')
    utility = UtilitySerializer(many=False, required=True, source='get_utility')
    document_type = DocumentTypeSerializer(many=False, required=True, source='get_type')
    document_sub_type = DocumentSubTypeSerializer(many=False, required=True, source='get_sub_type')
    created_date = serializers.SerializerMethodField('get_created_date')

    class Meta:
        model = DocumentTbl
        fields = ('id_string', 'tenant', 'utility', 'document_type', 'document_sub_type', 'name', 'link',
                  'is_active','created_date')

    def create(self, validated_data, user):
        document = super(DocumentSerializer, self).create(validated_data)
        document.created_by = user
        document.save()
        return document