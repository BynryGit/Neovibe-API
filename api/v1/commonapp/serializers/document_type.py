__author__ = "Arpita"


from rest_framework import serializers, status
from v1.tenant.models.tenant_region import TenantRegion as TenantRegionTbl
from v1.commonapp.models.document_type import DocumentType as DocumentTypeTbl
from django.db import transaction
from v1.commonapp.common_functions import set_document_type_validated_data
from datetime import datetime
from api.messages import DOCUMENT_TYPE_ALREADY_EXIST
from v1.commonapp.views.custom_exception import CustomAPIException
from v1.utility.models.utility_document_type import UtilityDocumentType as UtilityDocumentTypeTbl


class TenantRegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TenantRegionTbl
        fields = ('id_string', 'region')


class DocumentTypeViewSerializer(serializers.ModelSerializer):
    tenant = serializers.ReadOnlyField(source='tenant.name')
    tenant_id_string = serializers.ReadOnlyField(source='tenant.id_string')
    utility = serializers.ReadOnlyField(source='utility.name')
    utility_id_string = serializers.ReadOnlyField(source='utility.id_string')

    class Meta:
        model = UtilityDocumentTypeTbl
        fields = '__all__'


class DocumentTypeSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, max_length=200,
                                 error_messages={"required": "The field name is required."})
    utility_id = serializers.CharField(required=False, max_length=200)
    tenant_id = serializers.CharField(required=False, max_length=200)
    document_type_id = serializers.CharField(required=False, max_length=200)

    class Meta:
        model = UtilityDocumentTypeTbl
        fields = '__all__'

    def create(self, validated_data, user):
        with transaction.atomic():
            validated_data = set_document_type_validated_data(validated_data)
            if UtilityDocumentTypeTbl.objects.filter(name=validated_data['name'], tenant_id=validated_data['tenant_id'],
                                                     utility_id=validated_data['utility_id']).exists():
                raise CustomAPIException(DOCUMENT_TYPE_ALREADY_EXIST, status_code=status.HTTP_409_CONFLICT)
            else:

                document_type_obj = super(DocumentTypeSerializer, self).create(validated_data)
                document_type_obj.created_by = user.id
                document_type_obj.updated_by = user.id
                document_type_obj.save()
                return document_type_obj

    def update(self, instance, validated_data, user):
        validated_data = set_document_type_validated_data(validated_data)
        with transaction.atomic():
            document_type_obj = super(DocumentTypeSerializer, self).update(instance, validated_data)
            document_type_obj.tenant = user.tenant
            document_type_obj.updated_by = user.id
            document_type_obj.updated_date = datetime.utcnow()
            document_type_obj.save()
            return document_type_obj


class DocumentTypeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTypeTbl
        fields = ('name', 'id_string', 'is_active', 'created_by', 'created_date')
